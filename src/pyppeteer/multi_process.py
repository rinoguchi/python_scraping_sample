"""
pyppeteerを使うマルチプロセスサンプル
"""
import asyncio
from pyppeteer.launcher import launch
from pyppeteer.page import Page, Response
from pyppeteer.browser import Browser
from pyppeteer.element_handle import ElementHandle
from typing import List, Any

from concurrent import futures
from concurrent.futures import Future


def main():
    future_list: List[Future] = []
    htmls: List[str] = []
    with futures.ProcessPoolExecutor(max_workers=2) as executor:
        for i in range(10):
            future_list.append(executor.submit(pallalel_func))

        for future in futures.as_completed(fs=future_list):
            htmls.append(future.result())

    print(f'htmls count: {len(htmls)}')


def pallalel_func() -> str:
    return asyncio.get_event_loop().run_until_complete(extract_html())


async def extract_html() -> str:
    # ブラウザを起動。headless=Falseにすると実際に表示される
    browser: Browser = await launch(headless=False)
    try:
        page: Page = await browser.newPage()

        # ログイン画面に遷移
        response: Response = await page.goto('http://quotes.toscrape.com/login', waitUntil=['load', 'networkidle0'])
        if response.status != 200:
            raise RuntimeError(f'site is not available. status: {response.status}')

        # Username・Passwordを入力
        await page.type('#username', 'hoge')
        await page.type('#password', 'fuga')
        login_btn: ElementHandle = await page.querySelector('form input.btn')

        # Loginボタンクリック
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
