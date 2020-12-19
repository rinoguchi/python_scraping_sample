const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch(); // NOTE: headless=trueじゃないと、「UnhandledPromiseRejectionWarning: Error: Protocol error (Page.printToPDF): PrintToPDF is not implemented」が発生する
    const page = await browser.newPage();
    await page.goto('https://www.google.com/');
    await page.pdf({ path: 'downloads/sample2.pdf', format: 'A4' })
    await browser.close();
})();