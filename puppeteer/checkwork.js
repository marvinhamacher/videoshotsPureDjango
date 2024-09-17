const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.waitForSelector('h1');  // Test if this is recognized
  console.log('Title found');
  await browser.close();
})();