"""
pyppeteerを使って直接binaryファイルのダウンロードを試す=>!!!!!!うまく動かなかった!!!!!!

このプログラムを実行すると
pyppeteer.errors.NetworkError: Protocol error Network.getResponseBody: Target closed.
というエラーが発生する。getResponseBodyを実行しようとしたところ、すでにconnectionがクローズされてる模様。

https://github.com/miyakogi/pyppeteer/issues/171
を参照すると、websocketsライブラリのバージョンを6.0に戻せば行けると書いてあるが、
実際に古いバージョンをインストールしようとすると
pyppeteer (>=0.2.2,<0.3.0) requires websockets (>=8.1,<9.0).
と言われて、古いバージョンはインストールできない。
"""
import asyncio
from pyppeteer.launcher import launch
from pyppeteer.page import Page, Response, Request
from pyppeteer.browser import Browser


def main():
    asyncio.get_event_loop().run_until_complete(extract_content())


async def extract_content():
    # ブラウザを起動。headless=Falseにすると実際に表示される
    browser: Browser = await launch(headless=True)
    try:
        page: Page = await browser.newPage()
        await page.setRequestInterception(True)

        async def handle_request(request: Request):
            print('handle_request started.')
            await request.continue_()
            print('handle_request finished.')

        async def handle_response(response: Response):
            print('handle_response started.')
            print(f'content-type: {response.headers["content-type"]}')
            file_path: str = './test.pdf'
            file_content: bytes = await response.buffer()
            with open(file_path, 'wb') as f:
                f.write(file_content)
            print('handle_response fininshed.')

        page.on('request', lambda req: asyncio.ensure_future(handle_request(req)))
        page.on('response', lambda res: asyncio.ensure_future(handle_response(res)))

        await asyncio.gather(
            page.goto('https://www.mhlw.go.jp/www1/topics/kenko21_11/pdf/b2.pdf', waitUntil=['load', 'networkidle2']),
            page.waitForNavigation()
        )
    finally:
        await browser.close()


if __name__ == "__main__":
    main()
