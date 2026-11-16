const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const root = __dirname;
const app = path.join(root, 'app');
const configFile = path.join(root, 'config.local.json');
const config = fs.existsSync(configFile) ? JSON.parse(fs.readFileSync(configFile, 'utf8').replace(/^\uFEFF/, '')) : {};
const git = (args, cwd = root) => cp.execFileSync('git', args, { cwd, stdio: 'inherit' });
const mode = process.argv[2];
// This public-preview launcher pins new installs to a reviewed GitHub RC tag.
// Personal config can override source and ref, but neither is read from manuscripts.
const releaseRef = config.ref || 'preview-0.16.0-rc.1';
if (mode === 'prepare') {
  fs.rmSync(path.join(root, '.installed'), { force: true });
  if (!fs.existsSync(path.join(app, '.git'))) {
    if (fs.existsSync(app)) throw Error('app exists without Git metadata; refusing to overwrite');
    git(['clone', '--no-hardlinks', config.source || 'https://github.com/grumpystrongman/EmberWriter.git', 'app']);
    git(['checkout', '--detach', releaseRef], app);
  }
} else if (mode === 'update') {
  // Never reset local edits, switch branches, or rewrite history.
  const changes = cp.execFileSync('git', ['status', '--porcelain'], { cwd: app, encoding: 'utf8' }).trim();
  if (changes) throw Error('App contains local edits. Back up and review them before updating. No source files were overwritten.');
  let branch = '';
  try { branch = cp.execFileSync('git', ['symbolic-ref', '--quiet', '--short', 'HEAD'], { cwd: app, encoding: 'utf8' }).trim(); } catch { /* pinned prerelease tags use detached HEAD */ }
  if (branch) git(['pull', '--ff-only'], app);
  else {
    git(['fetch', '--tags', 'origin'], app);
    git(['checkout', '--detach', releaseRef], app);
  }
  if (fs.existsSync(path.join(root, '.git'))) {
    const remotes = cp.execFileSync('git', ['remote'], { cwd: root, encoding: 'utf8' }).trim();
    if (remotes) git(['pull', '--ff-only']);
    else console.log('Launcher has no remote; keeping installed launcher scripts.');
  }
} else if (mode === 'reset') {
  for (const relative of ['.installed', 'app/backend/env', 'app/frontend/node_modules', 'app/frontend/dist']) {
    const target = path.resolve(root, relative);
    if (!target.startsWith(root + path.sep)) throw Error('Unsafe reset path');
    fs.rmSync(target, { recursive: true, force: true, maxRetries: 20, retryDelay: 250 });
  }
} else throw Error('Expected prepare, update, or reset');
