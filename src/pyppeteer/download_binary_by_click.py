"""
pyppeteerを使ってリンククリックしてbinaryダウンロードするケースを試す=>!!!!!!うまく動かなかった!!!!!!
download_binary_directory.pyと同じ事象が発生。
"""
import asyncio
from pyppeteer.launcher import launch
from pyppeteer.page import Page, Response, Request, ElementHandle
from pyppeteer.browser import Browser


def main():
    asyncio.get_event_loop().run_until_complete(extract_content())


async def extract_content():
    # ブラウザを起動。headless=Falseにすると実際に表示される
    browser: Browser = await launch(headless=True)
    try:
        page: Page = await browser.newPage()
        # pdfリンクが存在するページに遷移
        await page.goto('https://www.mhlw.go.jp/www1/topics/kenko21_11/pdff.html', waitUntil=['load', 'networkidle0'])

        await page.setRequestInterception(True)

        async def handle_request(request: Request):
            print('handle_request started.')
            await request.continue_()
            print('handle_request finished.')

        async def handle_response(response: Response):
            print('handle_response started.')
            print(response.headers['content-type'])
            file_path: str = './test.pdf'
            file_content: bytes = await response.buffer()
            with open(file_path, 'wb') as f:
                f.write(file_content)
            print('handle_response fininshed.')

        page.on('request', lambda req: asyncio.ensure_future(handle_request(req)))
        page.on('response', lambda res: asyncio.ensure_future(handle_response(res)))

        pdf_link: ElementHandle = await page.querySelector('a[href="pdf/t0.pdf"]')
        await asyncio.gather(pdf_link.click(), page.waitForNavigation())

    finally:
        await browser.close()


if __name__ == "__main__":
    main()
