import operator
from typing import TypedDict, Annotated, List

class News(TypedDict):
    title: str
    date: str
    text: str
    link: str

class Trends(TypedDict):
    trends: List[News]

class Content(TypedDict, total=False):
    target_audience: str
    analytics: Annotated[List[Trends], operator.add]
    post_topic: str
    prompt: str
    summary: str
