import { chromium } from "playwright";
import path from "path";

(async () => {
  const browser = await chromium.launch();
  const outDir = "/opt/cursor/artifacts/screenshots";

  // Desktop — bottom trigger visible
  const desktop = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await desktop.goto("http://localhost:3456");
  await desktop.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await desktop.waitForTimeout(600);
  await desktop.screenshot({ path: path.join(outDir, "sha25-desktop-bottom.png") });

  // Desktop — sheet open
  await desktop.click('button:has-text("How this site was built")');
  await desktop.waitForTimeout(400);
  await desktop.screenshot({ path: path.join(outDir, "sha25-desktop-sheet.png") });
  await desktop.close();

  // Mobile — sheet open
  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mobile.goto("http://localhost:3456");
  await mobile.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await mobile.waitForTimeout(600);
  await mobile.click('button:has-text("How this site was built")');
  await mobile.waitForTimeout(400);
  await mobile.screenshot({ path: path.join(outDir, "sha25-mobile-sheet.png") });
  await mobile.close();

  await browser.close();
  console.log("Screenshots saved to", outDir);
})();
