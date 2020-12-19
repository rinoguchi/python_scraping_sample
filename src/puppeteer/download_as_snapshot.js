const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('https://www.google.com/');
    await page.screenshot({ path: 'downloads/sample1.png' })
    await browser.close();
})();