// Reset generated dependencies only; manuscripts and .ember settings survive.
module.exports = { run: [
  { method: "script.stop", params: { uri: "{{path.resolve(cwd, 'start-demo.js')}}" } },
  { method: "script.stop", params: { uri: "{{path.resolve(cwd, 'start.js')}}" } },
  { method: "shell.run", params: { message: "node setup.js reset" } },
  { method: "script.start", params: { uri: "install.js" } }
] };
