// Daemon + URL handoff: gepeto capture pattern and mochi/start.js.
module.exports = {
  daemon: true,
  run: [
    { method: "shell.run", params: {
      path: "app/backend", venv: "env",
      message: "python ../../serve.py --port {{port}}",
      on: [{ event: "/(http:\\/\\/[0-9.:]+)/", done: true }]
    } },
    { method: "local.set", params: { url: "{{input.event[1]}}" } }
  ]
};
