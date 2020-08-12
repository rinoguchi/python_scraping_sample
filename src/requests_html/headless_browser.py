"""
requests-htmlのエレメントクリックのサンプル
"""

from requests_html import HTMLSession
from requests import Response


def main():
    session: HTMLSession = HTMLSession()
    response: Response = session.get('https://qiita.com/')

    # == ヘッドレスブラウザで読み込み ==
    # レスポンスHTMLをヘッドレスブラウザで読み込み5秒待つ
    response.html.render(sleep=5)

    # == ヘッドレスブラウザで描画されれたHTMLを取得 ==
    response.html.raw_html
    # -> b'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Qiita</title>...</iframe></div></div></body></html>'

    # == ヘッドレスブラウザで描画されれたHTMLからCSSセレクタで要素を検索 ==
    response.html.find('.p-home_aside div[data-hyperapp-app="TagRanking"] .ra-TagList_content .ra-Tag_name a', first=True)
    # -> <Element 'a' href='/tags/python'>

    # == スクリプトを実行 ==
    # ユーザランキング週間一位をクリックして画面遷移
    response.html.render(script="""
            () => { document.querySelector('div[data-hyperapp-app="UserRanking"] .ra-UserList_content .ra-User_name > a').click() }
        """, sleep=5)
    # NOTE: sleepしないと、`pyppeteer.errors.NetworkError: Protocol error (Runtime.callFunctionOn): Cannot find context with specified id`が発生する

    # 画面遷移後のHTMLから要素を抽出
    response.html.find('a[href$="contributions"] > p[class^="UserCounterList__UserCounterItemCount"]', first=True).text
    # -> 60598

    # Contributionsリンクをクリックして画面遷移 => さらに画面遷移するのはできないっぽい
    # response.html.render(script="""
    #         () => { document.querySelector('a[href$="contributions"]').click() }
    #     """, sleep=5)
    # NOTE: `pyppeteer.errors.ElementHandleError: Evaluation failed: TypeError: Cannot read property 'click' of null が発生する`が発生する
    #       scriptの実行は最初にrenderしたHTMLに対して行われる模様。


if __name__ == "__main__":
    main()
