const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    async function downlaod(targetUrl) {
        const browser = await puppeteer.launch();
        const page = await browser.newPage(); // ページを開く
        const outputPath = `downloads/${targetUrl.match(/([^/]+\.[^/]+)($|\?)/)[1]}`; // URLからファイル名取得して、出力パス

        await page.setRequestInterception(true); // リクエストをインターセプトする。request.abortやrequest.continue、request.respondを自前で実装する必要あり
        let isFirstRequest = true;
        page.on('request', request => {
            if (!isFirstRequest && request.isNavigationRequest()) { // 初回リクエスト以外で画面遷移の場合は終了
                isFirstRequest = false;
                return request.abort();
            }
            request.continue(); // リクエストを継続する
        });
        page.on('response', async (response) => {
            if (response.url() === targetUrl) {
                const buffer = await response.buffer();
                fs.writeFile(outputPath, buffer, (err) => {
                    if (err) throw err;
                });
            }
        });

        await page.goto(targetUrl);
        await browser.close();
    }

    // HTML => OK
    await downlaod('https://www.soumu.go.jp/menu_syokai/index.html');
    // 画像 => OK
    await downlaod('https://www.soumu.go.jp/main_content/000269738.jpg');
    // CSV => NG: 「Error: Protocol error (Network.getResponseBody): No resource with given identifier found」が発生する。browser.on('targetcreated')を利用する必要がある
    await downlaod('https://www.soumu.go.jp/main_content/000608358.csv');
    // pdf => NG: 「Error: Protocol error (Network.getResponseBody): No resource with given identifier found」が発生する。browser.on('targetcreated')を利用する必要がある
    await downlaod('https://www.soumu.go.jp/main_content/000323620.pdf');
})();