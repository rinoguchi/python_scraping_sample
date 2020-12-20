"""
強制的にブラウザのファイルダウンロードを実行させる
"""
import asyncio
from typing import Dict

import pyppdf.patch_pyppeteer  # NOTE: chromiumのバージョンが古く、「pyppeteer.errors.NetworkError: Protocol error(Fetch.enable): 'Fetch.enable' wasn't found」が発生する問題の回避　  # noqa
from pyppeteer.launcher import launch
from pyppeteer.page import Page
from pyppeteer.element_handle import ElementHandle
from pyppeteer.browser import Browser


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

        await page._client.send('Page.setDownloadBehavior', {
            'behavior': 'allow',  # ダウンロードを許可
            'downloadPath': 'downloads'  # ダウンロード先のフォルダを指定
        })
        await page._client.send('Fetch.enable', {  # フェッチを有効に
            'patterns': [{'urlPattern': '*', 'requestStage': 'Request'}]  # NOTE: requestStageにResponseを指定するとなぜかイベントをキャプチャできない。しょうがないのでRequestをキャプチャする
        })

        async def request_paused_handler(request_event: Dict):
            request_id: str = request_event['requestId']
            response = await page._client.send('Fetch.getResponseBody', {'requestId': request_id})
            # ここで「pyppeteer.errors.NetworkError: Protocol error Fetch.getResponseBody: Target closed.」エラーが発生
            # Requestステージなのでダメなのは当たり前。やはりResponnseステージじゃないとダメだが解決方法が不明

        page._client.on('Fetch.requestPaused', request_paused_handler)

        link: ElementHandle = await page.querySelector(selector)
        await link.click()  # 対象リンクをクリック

    finally:
        await browser.close()


if __name__ == "__main__":
    main()
