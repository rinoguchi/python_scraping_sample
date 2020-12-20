"""
ファイルダウンロードリクエストをキャプチャして、別途リクエストを送信する
"""
from typing import Union, List, Dict
import asyncio
from uuid import uuid4
from mimetypes import guess_extension

from pyppeteer.launcher import launch
from pyppeteer.page import Page, Request
from pyppeteer.element_handle import ElementHandle
from pyppeteer.browser import Browser

import requests
from requests import Response


def main():
    asyncio.get_event_loop().run_until_complete(
        download('https://www.soumu.go.jp/toukei_toukatsu/index/seido/9-5.htm', 'a[href*=".csv"]'))
    asyncio.get_event_loop().run_until_complete(
        download('https://www.soumu.go.jp/toukei_toukatsu/index/seido/9-5.htm', 'a[href*=".pdf"]'))
    asyncio.get_event_loop().run_until_complete(
        download('https://pdf-xml-download-test.vercel.app/', '#link-pdf'))
    asyncio.get_event_loop().run_until_complete(
        download('https://pdf-xml-download-test.vercel.app/', '#link-xml'))


async def download(target_url: str, selector: str):
    browser: Browser = await launch(headless=True)
    try:
        page: Page = await browser.newPage()
        await asyncio.gather(page.goto(target_url), page.waitForNavigation())  # 対象ページに移動
        cookies: List[Dict[str, Union[str, int, bool]]] = await page.cookies()  # cookieを取得

        await page.setRequestInterception(True)  # リクエストをインターセプト
        page.on('request',
                lambda request: asyncio.create_task(send_request(request, cookies)))  # キャプチャした内容で別途リクエストを送信

        link: ElementHandle = await page.querySelector(selector)
        await link.click()  # 対象リンクをクリック

    finally:
        await browser.close()


async def send_request(request: Request, cookies: List[Dict[str, Union[str, int, bool]]]):
    response: Response = requests.request(
        url=request.url,
        method=request.method,
        headers=request.headers,
        cookies=dict(map(lambda cookie: (cookie['name'], cookie['value']), cookies)),
        data=request.postData,  # TODO: 要動作確認
    )
    extension: str = guess_extension(response.headers.get("content-type"))
    output_path: str = f'downloads/{uuid4()}{extension}'
    with open(output_path, mode='wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    main()
