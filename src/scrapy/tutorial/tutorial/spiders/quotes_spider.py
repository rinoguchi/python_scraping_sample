import scrapy
from typing import List


class QuotesSpider(scrapy.Spider):
    name: str = "quotes"

    def start_requests(self):
        urls: List[str] = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page: str = response.url.split("/")[-2]
        filename: str = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
