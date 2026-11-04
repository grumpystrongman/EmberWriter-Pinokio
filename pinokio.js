// Independent demo and personal workspaces, each with its own loopback URL.
module.exports = {
  version: "8.0.0",
  title: "EmberWriter",
  description: "Local-first fiction studio — separate Demo and Private workspaces",
  menu: async (kernel, info) => {
    for (const [script, title] of [["install.js", "Installing"], ["update.js", "Updating"], ["reset.js", "Rebuilding dependencies"], ["models.js", "Installing writing model"]]) {
      if (info.running(script)) return [{ default: true, text: title, href: script }];
    }
    if (!info.exists(".installed")) return [{ default: true, text: "Install", href: "install.js" }];
    const personalOn = info.running("start.js");
    const demoOn = info.running("start-demo.js");
    const personal = info.local("start.js");
    const demo = info.local("start-demo.js");
    return [
      demoOn
        ? (demo && demo.url
          ? { default: true, text: "Open DEMO (sample stories only)", href: demo.url }
          : { default: true, text: "Demo startup terminal", href: "start-demo.js" })
        : { default: true, text: "Start DEMO (sample stories only)", href: "start-demo.js" },
      ...(demoOn ? [{ text: "Stop DEMO", href: "stop-demo.js" }] : []),
      personalOn
        ? (personal && personal.url
          ? { text: "Open PRIVATE (your manuscripts)", href: personal.url }
          : { text: "Private startup terminal", href: "start.js" })
        : { text: "Start PRIVATE (your manuscripts)", href: "start.js" },
      ...(personalOn ? [{ text: "Stop PRIVATE", href: "stop.js" }] : []),
      { text: "Update", href: "update.js" },
      { text: "Install writing model (if missing)", href: "models.js" },
      { text: "Reinstall dependencies", href: "reset.js" },
      { text: "Instructions", href: "README.md" }
    ];
  }
};