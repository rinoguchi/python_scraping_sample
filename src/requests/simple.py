"""
requestsのシンプルなサンプル
"""

import requests
from requests import Response


def main():
    response: Response = requests.get('http://quotes.toscrape.com/')

    print(f'response.status_code: {response.status_code}')
    print(f'response.headers: {response.headers}')
    print(f'response.text: {response.text}')


if __name__ == "__main__":
    main()
