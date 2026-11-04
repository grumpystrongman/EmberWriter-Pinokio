const assert = require("node:assert/strict");
const launcher = require("./pinokio");
const personal = require("./start");
const demo = require("./start-demo");
(async () => {
  const state = (installed, active = [], urls = {}) => ({
    exists: () => installed, running: script => active.includes(script),
    local: script => urls[script] || {}
  });
  const cases = [
    [state(false), "install.js"],
    [state(false, ["install.js"]), "install.js"],
    [state(true), "start-demo.js"],
    [state(true, ["start-demo.js"]), "start-demo.js"],
    [state(true, ["start-demo.js"], {"start-demo.js": {url: "http://127.0.0.1:42005"}}), "http://127.0.0.1:42005"],
    [state(true, ["start.js"], {"start.js": {url: "http://127.0.0.1:42004"}}), "start-demo.js"],
    [state(true, ["start.js", "start-demo.js"], {"start.js": {url: "http://127.0.0.1:42004"}, "start-demo.js": {url: "http://127.0.0.1:42005"}}), "http://127.0.0.1:42005"],
    [state(true, ["update.js"]), "update.js"],
    [state(true, ["reset.js"]), "reset.js"]
  ];
  for (const [info, expected] of cases) {
    const menu = await launcher.menu(null, info);
    assert.equal(menu.filter(item => item.default).length, 1);
    assert.equal(menu.find(item => item.default).href, expected);
  }
  for (const [script, mode] of [[personal, "personal"], [demo, "demo"]]) {
    const event = script.run[0].params.on[0].event;
    const regex = new RegExp(event.slice(1, -1));
    assert.equal("Uvicorn running on http://127.0.0.1:12345 (Press CTRL+C to quit)".match(regex)[1], "http://127.0.0.1:12345");
    assert.equal(script.run[1].params.url, "{{input.event[1]}}");
    if (mode === "demo") assert.match(script.run[0].params.message, /--mode demo/);
  }
  assert.match(require("./stop-demo").run[0].params.uri, /start-demo.js/);
  assert.match(require("./stop").run[0].params.uri, /start.js/);
  for (const script of ["update", "reset"]) {
    const stops = require("./" + script).run.filter(x => x.method === "script.stop");
    assert.equal(stops.length, 2);
    assert.ok(stops.some(x => x.params.uri.includes("start-demo.js")));
    assert.ok(stops.some(x => x.params.uri.includes("start.js")));
  }
  console.log("Private/demo menu, isolation mode, and launcher script checks passed");
})().catch(error => { console.error(error); process.exitCode = 1; });
