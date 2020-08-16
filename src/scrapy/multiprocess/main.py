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


def start_crawl(settings: Dict[str, Any], urls: List[str]):
    process: CrawlerProcess = CrawlerProcess(settings=settings)
    process.crawl(MySpider, urls)
    process.start()  # the script will block here until the crawling is finished


def main():
    # スクレイピング設定 see: https://docs.scrapy.org/en/latest/topics/settings.html
    settings: Dict[str, Any] = {
        'DOWNLOAD_DELAY': 3,
        'TELNETCONSOLE_ENABLED': False,
    }

    # クローリング実行
    from multiprocessing import Process

    Process(target=start_crawl, args=(settings, ['http://quotes.toscrape.com/page/1/'])).start()
    Process(target=start_crawl, args=(settings, ['http://quotes.toscrape.com/page/2/', 'http://quotes.toscrape.com/page/3/'])).start()


if __name__ == "__main__":
    main()
