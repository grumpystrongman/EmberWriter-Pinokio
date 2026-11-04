module.exports = { requires: { bundle: "ai" }, run: [
  { method: "shell.run", params: {
    path: "app/backend", venv: "env", message: "python ../../manage.py models"
  } }
] };
