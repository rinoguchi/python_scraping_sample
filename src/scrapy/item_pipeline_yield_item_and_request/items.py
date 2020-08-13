from dataclasses import dataclass


@dataclass
class MyItem:
    url: str
    status: int
    title: str
    body: str
