"""
pyppeteerを使うシンプルなサンプル
"""
import asyncio
from pyppeteer.launcher import launch
from pyppeteer.page import Page, Response
from pyppeteer.browser import Browser
from pyppeteer.element_handle import ElementHandle
from typing import List, Any


def main():
    html: str = asyncio.get_event_loop().run_until_complete(extract_html())
    print(html)


async def extract_html() -> str:
    # ブラウザを起動。headless=Falseにすると実際に表示される
    browser: Browser = await launch()
    try:
        page: Page = await browser.newPage()

        # ログイン画面に遷移
        response: Response = await page.goto('http://quotes.toscrape.com/login', waitUntil=['load', 'networkidle0'])
        if response.status != 200:
            raise RuntimeError(f'site is not available. status: {response.status}')

        # Username・Passwordを入力
        await page.type('#username', 'hoge')
        await page.type('#password', 'fuga')

        # Loginボタンクリック
        login_btn: ElementHandle = await page.querySelector('form input.btn')
        results: List[Any] = await asyncio.gather(login_btn.click(), page.waitForNavigation())
        if results[1].status != 200:
            raise RuntimeError(f'site is not available. status: {response.status}')

        # ログイン後の画面のHTML取得
        html: str = await page.content()

        return html
    finally:
        await browser.close()


if __name__ == "__main__":
    main()
