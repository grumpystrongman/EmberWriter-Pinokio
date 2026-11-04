// Structure: prototype/system/examples/browser-use/install.js; mochi/install.js.
module.exports = {
  requires: { bundle: "ai" },
  run: [
    { method: "shell.run", params: { message: "node setup.js prepare" } },
    { method: "shell.run", params: {
      path: "app/backend", venv: "env", venv_python: "3.11",
      message: 'uv pip install -e .'
    } },
    { method: "shell.run", params: {
      path: "app/frontend", env: { VITE_API_BASE_URL: "/api" },
      message: ["npm ci", "npm run build"]
    } },
    { method: "shell.run", params: {
      path: "app/backend", venv: "env", message: "python ../../manage.py install"
    } },
    { method: "shell.run", params: {
      path: "app/backend", venv: "env", message: "python ../../seed_showcase.py --offline"
    } }
  ]
};
