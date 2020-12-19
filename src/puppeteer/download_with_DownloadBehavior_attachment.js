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

        await client.send('Fetch.enable', { // Fetchを有効に
            patterns: [{ urlPattern: '*', requestStage: 'Response' }] // ResponseステージをFetch
        });

        await client.on('Fetch.requestPaused', async (requestEvent) => { // ここで要求を一時停止
            const { requestId } = requestEvent;
            let responseHeaders = requestEvent.responseHeaders || [];
            let contentType = responseHeaders.filter(
                header => header.name.toLowerCase() === 'content-type')[0].value;

            // pdfとxml以外はそのまま
            if (!contentType.endsWith('pdf') && !contentType.endsWith('xml')) {
                await client.send('Fetch.continueRequest', { requestId }); // リクエストを続行
                return;
            }

            // pdfとxmlの場合は`content-disposition: attachment`をつける
            responseHeaders.push({ name: 'content-disposition', value: 'attachment' });
            const response = await client.send('Fetch.getResponseBody', { requestId }); // bodyを取得
            await client.send('Fetch.fulfillRequest', // レスポンスを指定
                { requestId, responseCode: 200, responseHeaders, body: response.body });
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