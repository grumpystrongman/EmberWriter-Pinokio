// Separate demo server and data root; never mounts the personal library.
module.exports = {
  daemon: true,
  run: [
    { method: "shell.run", params: {
      path: "app/backend", venv: "env",
      message: "python ../../serve.py --mode demo --port {{port}}",
      on: [{ event: "/(http:\\/\\/[0-9.:]+)/", done: true }]
    } },
    { method: "local.set", params: { url: "{{input.event[1]}}" } }
  ]
};