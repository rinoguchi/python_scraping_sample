from scrapy.http import Response
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import SitemapSpider
from typing import Dict, Any


class MySitemapSpider(SitemapSpider):
    name = 'my_sitemap_spider'
    sitemap_urls = ['https://qiita.com/robots.txt']  # sitemap.xmlやrobots.txtを指定する

    def parse(self, response: Response):
        print(f'response.url: {response.url}')


def main():
    settings: Dict[str, Any] = {
        'DOWNLOAD_DELAY': 3,
        'TELNETCONSOLE_ENABLED': False,
    }

    # クローリング実行
    process: CrawlerProcess = CrawlerProcess(settings=settings)
    process.crawl(MySitemapSpider)
    process.start()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
