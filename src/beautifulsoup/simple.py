"""
BeautifulSoupのシンプルなサンプル
"""

import requests
from requests import Response
from bs4 import BeautifulSoup


def main():
    response: Response = requests.get('http://quotes.toscrape.com/')
    soup: BeautifulSoup = BeautifulSoup(response.text)

    # == タグをたどってエレメントを取得する ==
    print(f'{soup.title}')
    # -> <title>Quotes to Scrape</title>
    print(f'{soup.title.parent}')
    # -> <head><meta charset="utf-8"/><title>Quotes to Scrape</title><link href="/static/bootstrap.min.css" rel="stylesheet"/><link href="/static/main.css" rel="stylesheet"/></head>  # noqa
    print(f'{soup.body.footer.div.p.a}')
    # -> <a href="https://www.goodreads.com/quotes">GoodReads.com</a>

    # == find, find_allでタグを探してエレメントを取得する ==
    print(f'{soup.find("title")}')
    # -> <title>Quotes to Scrape</title>
    print(f'{soup.find_all("a")}')
    # -> [<a href="/" style="text-decoration: none">Quotes to Scrape</a>, <a href="/login">Login</a>, <a href="/author/Albert-Einstein">(about)</a>, <a class="tag" href="/tag/change/page/1/">change</a>, <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>, <a class="tag" href="/tag/thinking/page/1/">thinking</a>, <a class="tag" href="/tag/world/page/1/">world</a>, <a href="/author/J-K-Rowling">(about)</a>, <a class="tag" href="/tag/abilities/page/1/">abilities</a>, <a class="tag" href="/tag/choices/page/1/">choices</a>, <a href="/author/Albert-Einstein">(about)</a>, <a class="tag" href="/tag/inspirational/page/1/">inspirational</a>, <a class="tag" href="/tag/life/page/1/">life</a>, <a class="tag" href="/tag/live/page/1/">live</a>, <a class="tag" href="/tag/miracle/page/1/">miracle</a>, <a class="tag" href="/tag/miracles/page/1/">miracles</a>, <a href="/author/Jane-Austen">(about)</a>, <a class="tag" href="/tag/aliteracy/page/1/">aliteracy</a>, <a class="tag" href="/tag/books/page/1/">books</a>, <a class="tag" href="/tag/classic/page/1/">classic</a>, <a class="tag" href="/tag/humor/page/1/">humor</a>, <a href="/author/Marilyn-Monroe">(about)</a>, <a class="tag" href="/tag/be-yourself/page/1/">be-yourself</a>, <a class="tag" href="/tag/inspirational/page/1/">inspirational</a>, <a href="/author/Albert-Einstein">(about)</a>, <a class="tag" href="/tag/adulthood/page/1/">adulthood</a>, <a class="tag" href="/tag/success/page/1/">success</a>, <a class="tag" href="/tag/value/page/1/">value</a>, <a href="/author/Andre-Gide">(about)</a>, <a class="tag" href="/tag/life/page/1/">life</a>, <a class="tag" href="/tag/love/page/1/">love</a>, <a href="/author/Thomas-A-Edison">(about)</a>, <a class="tag" href="/tag/edison/page/1/">edison</a>, <a class="tag" href="/tag/failure/page/1/">failure</a>, <a class="tag" href="/tag/inspirational/page/1/">inspirational</a>, <a class="tag" href="/tag/paraphrased/page/1/">paraphrased</a>, <a href="/author/Eleanor-Roosevelt">(about)</a>, <a class="tag" href="/tag/misattributed-eleanor-roosevelt/page/1/">misattributed-eleanor-roosevelt</a>, <a href="/author/Steve-Martin">(about)</a>, <a class="tag" href="/tag/humor/page/1/">humor</a>, <a class="tag" href="/tag/obvious/page/1/">obvious</a>, <a class="tag" href="/tag/simile/page/1/">simile</a>, <a href="/page/2/">Next <span aria-hidden="true">→</span></a>, <a class="tag" href="/tag/love/" style="font-size: 28px">love</a>, <a class="tag" href="/tag/inspirational/" style="font-size: 26px">inspirational</a>, <a class="tag" href="/tag/life/" style="font-size: 26px">life</a>, <a class="tag" href="/tag/humor/" style="font-size: 24px">humor</a>, <a class="tag" href="/tag/books/" style="font-size: 22px">books</a>, <a class="tag" href="/tag/reading/" style="font-size: 14px">reading</a>, <a class="tag" href="/tag/friendship/" style="font-size: 10px">friendship</a>, <a class="tag" href="/tag/friends/" style="font-size: 8px">friends</a>, <a class="tag" href="/tag/truth/" style="font-size: 8px">truth</a>, <a class="tag" href="/tag/simile/" style="font-size: 6px">simile</a>, <a href="https://www.goodreads.com/quotes">GoodReads.com</a>, <a href="https://scrapinghub.com">Scrapinghub</a>]  # noqa

    # == CSSセレクタでエレメントを取得する ==
    print(f'{soup.select("body .container .row .quote small.author")}')
    # -> [<small class="author" itemprop="author">Albert Einstein</small>, <small class="author" itemprop="author">J.K. Rowling</small>, <small class="author" itemprop="author">Albert Einstein</small>, <small class="author" itemprop="author">Jane Austen</small>, <small class="author" itemprop="author">Marilyn Monroe</small>, <small class="author" itemprop="author">Albert Einstein</small>, <small class="author" itemprop="author">André Gide</small>, <small class="author" itemprop="author">Thomas A. Edison</small>, <small class="author" itemprop="author">Eleanor Roosevelt</small>, <small class="author" itemprop="author">Steve Martin</small>]  # noqa
    print(f'{soup.select("body .container .row div.quote:first-child small.author")}')
    # -> [<small class="author" itemprop="author">Albert Einstein</small>]
    print(f'{soup.select("body .container .row div.quote:last-of-type small.author")}')
    # -> [<small class="author" itemprop="author">Steve Martin</small>]

    # == エレメントの属性情報を取得する ==
    print(f'{soup.title.string}')
    # -> Quotes to Scrape
    print(f'{soup.title.name}')
    # -> title
    print(f'{soup.body.footer.div.p.a["href"]}')
    # -> https://www.goodreads.com/quotes

    # == 正規表現でテキストを抽出する ==
    import re
    print(f'{soup.find_all(text=re.compile("^“A "))}')
    # -> ["“A woman is like a tea bag; you never know how strong it is until it's in hot water.”", '“A day without sunshine is like, you know, night.”'] # noqa


if __name__ == "__main__":
    main()
