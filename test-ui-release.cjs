"use strict";
/*
 * Release-only hosted UI smoke. Requires an explicitly isolated Pinokio QA
 * server, preinstalled Playwright core and Edge/Chromium. Never connects to
 * live personal Pinokio folders or any author data.
 *
 * EMBER_PINOKIO_QA_URL=http://127.0.0.1:<testport> node test-ui-release.cjs
 * NODE_PATH may point to an existing QA-only node_modules installation.
 */
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");

async function main() {
  const url = process.env.EMBER_PINOKIO_QA_URL || "";
  if (!/^http:\/\/127\.0\.0\.1:\d+$/.test(url))
    throw new Error("Only explicit loopback QA servers can be UI-tested");
  const root = __dirname;
  if (!/qa/i.test(root) || !fs.existsSync(path.join(root, ".installed")))
    throw new Error("UI QA cannot inspect a non-isolated personal Pinokio install");
  const { chromium } = require("playwright-core");
  const edge = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
  if (!fs.existsSync(edge))
    throw new Error("Headless Edge not installed on this Windows test host");
  const browser = await chromium.launch({
    executablePath: edge, headless: true,
    args: ["--disable-extensions", "--no-sandbox"],
  });
  try {
    const page = await browser.newPage({
      viewport: {width: 1600, height: 900}, deviceScaleFactor: 1,
    });
    const errs = [];
    page.on("pageerror", e => errs.push("JS: " + e.message));
    page.on("response", response => {
      if (response.status() >= 400 && response.url().includes("/api/"))
        errs.push(response.status() + " " + response.url());
    });
    await page.goto(url, {waitUntil: "domcontentloaded"});
    await page.waitForTimeout(1400);
    assert(await page.title(), "Missing title");
    const nav = page.locator(".workspace-nav button");
    assert((await nav.count()) >= 4, "Writing workspace navigation disappeared");
    const series = nav.filter({hasText: "Series"});
    assert(await series.count(), "Series workspace is missing");
    await series.first().click();
    await page.locator(".series-desk-tabs").waitFor({timeout: 12000});
    const tabs = await page.locator(".series-desk-tabs button").allTextContents();
    for (const title of ["Continuity", "Consequences", "Ask Ember"]) {
      assert(tabs.some(label => label.includes(title)), "Missing author tool: " + title);
    }
    await page.locator(".series-desk-tabs button").filter({hasText: "Continuity"}).click();
    await page.locator(".series-pro").waitFor();
    await page.screenshot({path: path.join(root, "qa-ui-desktop.png"),
                           animations: "disabled"});
    await page.setViewportSize({width: 390, height: 844});
    await page.waitForTimeout(700);
    const mobile = await page.evaluate(() => {
      const a = document.querySelector(".load-import-launcher")?.getBoundingClientRect();
      const b = document.querySelector(".ember-companion-launcher")?.getBoundingClientRect();
      const overlapping = !!(a && b && a.left < b.right && a.right > b.left
        && a.top < b.bottom && a.bottom > b.top);
      return {
        viewport: innerWidth, width: document.documentElement.scrollWidth,
        binderCollapsed: document.querySelector(".workspace-shell")?.classList.contains("binder-collapsed"),
        floatingControlsOverlap: overlapping,
      };
    });
    assert(mobile.width <= mobile.viewport + 2,
           "Hosted Pinokio app has mobile horizontal overflow: " + JSON.stringify(mobile));
    assert(mobile.binderCollapsed,
           "Binder covers mobile writing content: " + JSON.stringify(mobile));
    assert(!mobile.floatingControlsOverlap,
           "Floating helper hides mobile import button: " + JSON.stringify(mobile));
    await page.screenshot({path: path.join(root, "qa-ui-mobile.png"),
                           animations: "disabled"});
    assert.equal(errs.length, 0, "UI/API errors: " + errs.join("; "));
    console.log(JSON.stringify({
      passed: true, hostedUI: true, synthetic: true,
      desktop: "1600x900", mobile: "390x844",
      ...mobile, errors: errs,
      screenshots: ["qa-ui-desktop.png", "qa-ui-mobile.png"],
    }, null, 2));
  } finally {
    await browser.close();
  }
}
main().catch(err => {console.error(err.stack || err); process.exitCode = 1});
