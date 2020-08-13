import scrapy
from scrapy.http import Response
from scrapy.crawler import CrawlerProcess
from typing import List, Dict, Any


class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, urls: List[str], *args, **kwargs):
        # Request対象のURLを指定
        self.start_urls = urls
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response: Response):
        page: str = response.url.split("/")[-2]
        filename: str = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


def main():
    # スクレイピング設定 see: https://docs.scrapy.org/en/latest/topics/settings.html
    settings: Dict[str, Any] = {
        'DOWNLOAD_DELAY': 3,
        'TELNETCONSOLE_ENABLED': False,
    }

    # クローリング実行
    process: CrawlerProcess = CrawlerProcess(settings=settings)
    process.crawl(MySpider, ['http://quotes.toscrape.com/page/1/', 'http://quotes.toscrape.com/page/2/'])
    process.start()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
