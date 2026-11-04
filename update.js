// Stop, back up, fast-forward app/launcher, then rebuild dependencies.
module.exports = { run: [
  { method: "script.stop", params: { uri: "{{path.resolve(cwd, 'start-demo.js')}}" } },
  { method: "script.stop", params: { uri: "{{path.resolve(cwd, 'start.js')}}" } },
  { method: "shell.run", params: {
    path: "app/backend", venv: "env", message: "python ../../manage.py backup"
  } },
  { method: "shell.run", params: { message: "node setup.js update" } },
  { method: "script.start", params: { uri: "install.js" } }
] };
