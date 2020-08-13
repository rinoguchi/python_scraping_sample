from scrapy.exceptions import DropItem
from scrapy import Spider
from items import MyItem


class StatusFilterPipeline:
    """ステータスでフィルターするパイプライン"""

    def process_item(self, item: MyItem, spider: Spider) -> MyItem:
        if item.status != 200:
            raise DropItem(f'Status is not 200. status: {item.status}')
        return item


class BodyLengthFilterPipeline:
    """BODYサイズでフィルターするパイプライン"""

    def process_item(self, item: MyItem, spider: Spider) -> MyItem:
        if len(item.body) < 11000:
            raise DropItem(f'Body length less than 11000. body_length: {len(item.body)}')
        return item


class OutputFilePipeline:
    """ファイル出力するパイプライン"""

    def process_item(self, item: MyItem, spider: Spider):
        filename: str = f'quotes-{item.url.split("/")[-2]}.html'
        with open(filename, 'wb') as f:
            f.write(item.body)
