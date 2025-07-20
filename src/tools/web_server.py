import time
from typing import Any

import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchResults
from mcp.server import FastMCP

from src.domain.state import Trends, News, Content


class WebTools:

    def __init__(self, web: FastMCP):
        self.web = web

        web.tool(
            name="mcp_web_parse",
            description="""
             Чтобы использовать инструмент необходимо - передать источники для парсинга

             В аргумент items инструмента веб парсинга источники прописываются через |AND| списком из 3-х элементов открытого текста, без цифр, таких как (1. 2.), или чего-либо еще, не связанного с запросом - ПРОСТО открытым ТЕКСТОМ в нижнем регистре.
             Между ссылками обязательно должны быть пробелы "  |AND|  "
            
             Пример:
             https://test1.com  |AND|  https://test2.com  |AND|  https://test3.com
         """,
        ) (self.parse)

    @staticmethod
    def parse(target_audience: str, items: str) -> dict | list[Any]:
        state = []

        try:
            # search = DuckDuckGoSearchResults(output_format="list")
            lines_array = items.strip().split("|AND|")
            news_trends = []
            #
            # for item in lines_array:
            #     webs = search.invoke(item)

            for web in lines_array:
                try:
                    response = requests.get(web.strip()) #["link"]
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text = ""
                    for post in soup.find_all('p'):
                        text += post.get_text()

                    news = News(title="", text=text, link=web, date=str(time.ctime(time.time())))
                    news_trends.append(news)
                except:
                    continue

            trends = Trends(trends=news_trends)
            content = Content(target_audience=target_audience, analytics=[trends])

            return content

        except Exception as e:
            print("\n")
            print(e)
            print("\n")

        return state
