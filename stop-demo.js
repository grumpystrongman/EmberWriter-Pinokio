module.exports = { run: [
  { method: "script.stop", params: { uri: "{{path.resolve(cwd, 'start-demo.js')}}" } }
] };