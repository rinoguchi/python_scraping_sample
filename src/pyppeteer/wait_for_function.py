"""
pyppeteerでwaitForFunctionを使うサンプル
"""
import asyncio
from pyppeteer.launcher import launch
from pyppeteer.page import Page, Response
from pyppeteer.browser import Browser
from typing import List, Any


def main():
    asyncio.get_event_loop().run_until_complete(wait_for_function())


async def wait_for_function():
    # ブラウザを起動。headless=Falseにすると実際に表示される
    browser: Browser = await launch(headless=False)
    try:
        page: Page = await browser.newPage()

        # 画面を表示してwaitForFunctionでしばらく待つ
        await asyncio.gather(
            page.goto('http://quotes.toscrape.com', waitUntil=['load', 'networkidle0']),
            page.waitForFunction('() => { return document.querySelector("li.next") != null; }')
        )
        # response: Response = results[0]
        # print(response.status)
    finally:
        await browser.close()


if __name__ == "__main__":
    main()
