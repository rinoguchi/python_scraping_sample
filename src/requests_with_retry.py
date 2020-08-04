"""
poetry add requests
"""

import requests
from requests import Response, Session
from requests.exceptions import RequestException, Timeout
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict


def request():
    response: Response = requests.get('http://quotes.toscrape.com/')

    print(f'response.status_code: {response.status_code}')
    print(f'response.headers: {response.headers}')
    print(f'response.text: {response.text}')


def request_with_retry():
    with Session() as session:
        url: str = 'http://quotes.toscrape.com/'
        headers: Dict[str, str] = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept': '*/*'}  # noqa
        retries: Retry = Retry(total=5,  # リトライ回数
                               backoff_factor=3,  # リトライ間隔。例えば2を指定すると 2秒 => 4秒 => 8秒 => 16秒のようになる
                               status_forcelist=[500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511],  # リトライ対象のステータスコード
                               raise_on_status=False  # `retry_status_forcelist`のステータスコードでリトライ終了した場合にエラーraiseするかどうか。FalseだとResponseを返す
                               )

        session.mount(url[0:url.find('//') + 2], HTTPAdapter(max_retries=retries))

        try:
            response: Response = session.get(url, headers=headers)
            print(f'response.status_code: {response.status_code}')
            print(f'response.headers: {response.headers}')
            print(f'response.text: {response.text}')

        except (RequestException, ConnectionError, Timeout) as e:
            print(f'possible error occurred. {e}')


if __name__ == "__main__":
    request()
    request_with_retry()
