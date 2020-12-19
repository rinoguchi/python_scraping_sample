const puppeteer = require('puppeteer');

(async () => {
    async function sleep(msec) {
        setTimeout(() => { }, msec);
    }
    async function download(pageUrl, selector) {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(pageUrl);
        client = await page.target().createCDPSession();
        client.send('Page.setDownloadBehavior', {
            behavior: 'allow', // ダウンロードを許可
            downloadPath: 'downloads', // ダウンロード先のフォルダを指定
        });
        await page.click(selector);
        await sleep(5000); // ダウンロード完了を待つ
        await browser.close();
    }
    await download('https://www.soumu.go.jp/toukei_toukatsu/index/seido/9-5.htm', 'a[href*=".csv"]'); // OK
    await download('https://www.soumu.go.jp/toukei_toukatsu/index/seido/9-5.htm', 'a[href*=".pdf"]'); // OK
    await download('https://pdf-xml-download-test.vercel.app/', '#link-pdf'); // OK
    await download('https://pdf-xml-download-test.vercel.app/', '#link-xml'); // NG
})();