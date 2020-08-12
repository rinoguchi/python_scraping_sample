"""
requests-htmlのシンプルなサンプル
"""

from requests_html import HTMLSession
from requests import Response


def main():
    session: HTMLSession = HTMLSession()
    response: Response = session.get('http://quotes.toscrape.com/')

    # == Responseオブジェクトを取得する ==
    response.status_code
    # -> 200
    response.headers
    # -> {'Server': 'nginx/1.14.0 (Ubuntu)', 'Date': 'Tue, 11 Aug 2020 13:11:10 GMT', 'Content-Type': 'text/html; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'X-Upstream': 'spidyquotes-master_web', 'X-Content-Encoding-Over-Network': 'gzip'}  # noqa
    response.text
    # -> <!DOCTYPE html><html lang="en"><head>...</head><body>...</body></html>

    # == CSSセレクターを使ってエレメント抽出する ==
    # 全て抽出
    response.html.find("body .container .row .quote small.author")
    # -> [<Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>, <Element 'small' class=('author',) itemprop='author'>]  # noqa
    response.html.find("body .container .row div.quote:first-child small.author")
    # -> [<Element 'small' class=('author',) itemprop='author'>]
    response.html.find("body .container .row div.quote:last-of-type small.author")
    # -> [<Element 'small' class=('author',) itemprop='author'>]

    # 最初の1件抽出
    response.html.find("body .container .row .quote small.author", first=True)
    # -> <Element 'small' class=('author',) itemprop='author'>

    # == エレメントの属性情報を取得する ==
    response.html.find("body .container .row .quote a", first=True).attrs['href']
    # -> /author/Albert-Einstein
    response.html.find("body .container .row .quote small.author", first=True).text
    # -> Albert Einstein

    # == ページ内のリンクを全て取得する ==
    response.html.absolute_links
    # -> {'http://quotes.toscrape.com/author/Jane-Austen', 'http://quotes.toscrape.com/author/Steve-Martin', 'http://quotes.toscrape.com/tag/obvious/page/1/', 'http://quotes.toscrape.com/tag/choices/page/1/', 'http://quotes.toscrape.com/author/Albert-Einstein', 'http://quotes.toscrape.com/tag/life/page/1/', 'http://quotes.toscrape.com/', 'http://quotes.toscrape.com/author/Marilyn-Monroe', 'http://quotes.toscrape.com/tag/humor/page/1/', 'http://quotes.toscrape.com/tag/miracles/page/1/', 'http://quotes.toscrape.com/tag/thinking/page/1/', 'http://quotes.toscrape.com/author/Eleanor-Roosevelt', 'http://quotes.toscrape.com/tag/adulthood/page/1/', 'http://quotes.toscrape.com/tag/life/', 'http://quotes.toscrape.com/tag/world/page/1/', 'http://quotes.toscrape.com/tag/deep-thoughts/page/1/', 'http://quotes.toscrape.com/tag/friends/', 'http://quotes.toscrape.com/tag/miracle/page/1/', 'http://quotes.toscrape.com/author/Andre-Gide', 'http://quotes.toscrape.com/tag/change/page/1/', 'http://quotes.toscrape.com/tag/classic/page/1/', 'http://quotes.toscrape.com/tag/misattributed-eleanor-roosevelt/page/1/', 'http://quotes.toscrape.com/tag/love/', 'http://quotes.toscrape.com/tag/reading/', 'http://quotes.toscrape.com/tag/success/page/1/', 'http://quotes.toscrape.com/tag/paraphrased/page/1/', 'http://quotes.toscrape.com/tag/books/page/1/', 'http://quotes.toscrape.com/tag/truth/', 'http://quotes.toscrape.com/tag/live/page/1/', 'https://www.goodreads.com/quotes', 'http://quotes.toscrape.com/tag/inspirational/', 'http://quotes.toscrape.com/author/Thomas-A-Edison', 'http://quotes.toscrape.com/tag/love/page/1/', 'http://quotes.toscrape.com/tag/inspirational/page/1/', 'http://quotes.toscrape.com/login', 'http://quotes.toscrape.com/tag/edison/page/1/', 'http://quotes.toscrape.com/tag/books/', 'http://quotes.toscrape.com/tag/humor/', 'http://quotes.toscrape.com/tag/simile/', 'http://quotes.toscrape.com/tag/value/page/1/', 'https://scrapinghub.com', 'http://quotes.toscrape.com/tag/abilities/page/1/', 'http://quotes.toscrape.com/tag/failure/page/1/', 'http://quotes.toscrape.com/tag/simile/page/1/', 'http://quotes.toscrape.com/page/2/', 'http://quotes.toscrape.com/tag/be-yourself/page/1/', 'http://quotes.toscrape.com/tag/aliteracy/page/1/', 'http://quotes.toscrape.com/author/J-K-Rowling', 'http://quotes.toscrape.com/tag/friendship/'}  # noqa
    response.html.links
    # -> {'/tag/live/page/1/', '/author/Jane-Austen', '/tag/aliteracy/page/1/', '/page/2/', '/tag/choices/page/1/', '/tag/reading/', '/', '/tag/failure/page/1/', '/login', '/tag/simile/', '/author/Marilyn-Monroe', '/tag/love/page/1/', '/author/Steve-Martin', '/tag/adulthood/page/1/', '/tag/inspirational/page/1/', '/tag/world/page/1/', '/tag/obvious/page/1/', '/author/Eleanor-Roosevelt', '/tag/be-yourself/page/1/', '/tag/change/page/1/', '/tag/abilities/page/1/', '/tag/life/', '/tag/books/', '/tag/friendship/', '/tag/books/page/1/', '/tag/life/page/1/', '/tag/humor/page/1/', '/tag/truth/', '/tag/paraphrased/page/1/', '/tag/inspirational/', '/tag/friends/', 'https://www.goodreads.com/quotes', '/tag/simile/page/1/', '/tag/deep-thoughts/page/1/', '/author/Albert-Einstein', '/tag/love/', '/tag/miracles/page/1/', '/tag/miracle/page/1/', '/tag/thinking/page/1/', '/tag/misattributed-eleanor-roosevelt/page/1/', '/tag/value/page/1/', 'https://scrapinghub.com', '/author/Andre-Gide', '/tag/humor/', '/tag/classic/page/1/', '/tag/success/page/1/', '/tag/edison/page/1/', '/author/J-K-Rowling', '/author/Thomas-A-Edison'}  # noqa


if __name__ == "__main__":
    main()
