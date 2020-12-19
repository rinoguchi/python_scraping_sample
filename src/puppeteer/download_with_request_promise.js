const puppeteer = require('puppeteer');
const rp = require('request-promise');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const mime = require('mime-types');

(async () => {
    // 対象ページ内の対象selectorをクリックしてファイルをダウンロード
    async function download(pageUrl, selector) {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto(pageUrl);
        await page.setRequestInterception(true); // リクエストをインターセプト
        page.on('request', async (request) => {
            await sendRequest(request, await page.cookies()); // キャプチャした内容で別途リクエストを送信
            request.abort(); // リクエストを終了
        });
        await page.click(selector);
        await browser.close();
    }

    // request-promiseを使って別途リクエストを送信
    async function sendRequest(request, cookies) {
        const options = {
            encoding: null,
            method: request._method,
            uri: request._url,
            body: request._postData,
            headers: request._headers,
            resolveWithFullResponse: true, // content-typeを取得したいので、FullResponseを取得する設定
        }
        options.headers.Cookie = cookies.map(cookie => cookie.name + '=' + cookie.value).join(';');
        const response = await rp(options);
        const outputPath = `downloads/${uuidv4()}.${mime.extension(response.headers['content-type'])}`;
        fs.writeFile(outputPath, response.body, () => { }); // ファイルに出力
    }

    await download('https://www.soumu.go.jp/toukei_toukatsu/index/seido/9-5.htm', 'a[href*=".csv"]'); // OK
    await download('https://www.soumu.go.jp/toukei_toukatsu/index/seido/9-5.htm', 'a[href*=".pdf"]'); // OK
    await download('https://pdf-xml-download-test.vercel.app/', '#link-pdf'); // OK
    await download('https://pdf-xml-download-test.vercel.app/', '#link-xml'); // OK
})();