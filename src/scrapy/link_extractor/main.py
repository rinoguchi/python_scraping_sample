from scrapy.http import Response
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from typing import Dict, Any


class MyLinkExtractSpider(CrawlSpider):
    name = 'my_link_extract_spider'
    start_urls = ['http://quotes.toscrape.com/']
    rules = (
        Rule(
            LinkExtractor(
                allow=r'http://quotes.toscrape.com/page/\d+/',
                unique=True,
                tags=['a'],
            ),
            follow=True,
            callback='log_url'
        ),
    )

    def log_url(self, response: Response):
        print(f'response.url: {response.url}')


def main():
    # スクレイピング設定 see: https://docs.scrapy.org/en/latest/topics/settings.html
    settings: Dict[str, Any] = {
        'DOWNLOAD_DELAY': 3,
        'TELNETCONSOLE_ENABLED': False,
    }

    # クローリング実行
    process: CrawlerProcess = CrawlerProcess(settings=settings)
    process.crawl(MyLinkExtractSpider)
    process.start()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
