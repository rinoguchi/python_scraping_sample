from scrapy import Spider
from scrapy.http import Response
from scrapy.crawler import CrawlerProcess
from typing import List, Dict, Any, Iterator
from items import MyItem


class MySpider(Spider):
    name = 'my_spider'

    def __init__(self, urls: List[str], *args, **kwargs):
        # Request対象のURLを指定
        self.start_urls = urls
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response: Response) -> Iterator[MyItem]:
        yield MyItem(
            url=response.url,
            status=response.status,
            title=response.xpath('//title/text()').extract_first(),
            body=response.body,
        )


def main():
    # スクレイピング設定 see: https://docs.scrapy.org/en/latest/topics/settings.html
    settings: Dict[str, Any] = {
        'DOWNLOAD_DELAY': 3,
        'TELNETCONSOLE_ENABLED': False,
        'ITEM_PIPELINES': {
            'pipelines.StatusFilterPipeline': 100,
            'pipelines.BodyLengthFilterPipeline': 200,
            'pipelines.OutputFilePipeline': 300,
        },
    }

    # クローリング実行
    process: CrawlerProcess = CrawlerProcess(settings=settings)
    process.crawl(MySpider, ['http://quotes.toscrape.com/page/1/', 'http://quotes.toscrape.com/page/2/', 'http://quotes.toscrape.com/page/3/'])
    process.start()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
