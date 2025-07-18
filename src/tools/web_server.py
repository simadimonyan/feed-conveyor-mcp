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
            name="mcp_search",
            description="""
             Чтобы использовать инструмент необходимо - сгенерировать поисковые запросы для DuckDuckGo, чтобы найти самую свежую и актуальную
             информацию о целевой аудитории для создания поста в Telegram. Каждый запрос должен быть конкретным, своевременным,
             направленным на выявление тенденций, новостей или обсуждений, связанных с интересами, поведением или потребностями аудитории.
             Язык запроса должен соответствовать запросам целевой аудитории.
    
             Вот параметры для выполнения задачи:
             • Цель: собрать информацию о тенденциях или новостях, которые могут послужить основой для публикации, ориентированной на данную аудиторию.
             • Желаемые типы контента:
             • Последние новости или разработки.
             • Тенденции в сфере интересов аудитории.
             • Распространенные вопросы или обсуждения, происходящие в Интернете.
             • Инновационные идеи или продукты, ориентированные на аудиторию.
             
             В аргумент items инстпумента поиска запросы прописываются через \\n списком из 3-х элементов открытого текста, без цифр, таких как (1. 2.), или чего-либо еще, не связанного с запросом - ПРОСТО открытым ТЕКСТОМ в нижнем регистре.
             НЕ ВВОДИТЕ "Вот поисковые запросы для DuckDuckGo:" или что-то в этом роде
            
             Пример:
             запрос1 \\n запрос2 \\n запрос3
         """,
        ) (self.search)

    @staticmethod
    def search(target_audience: str, items: str) -> dict | list[Any]:
        state = []

        try:
            search = DuckDuckGoSearchResults(output_format="list")
            lines_array = items.split(" \n ")
            news_trends = []

            for item in lines_array:
                webs = search.invoke(item)

                for web in webs:
                    try:
                        response = requests.get(web["link"])
                        soup = BeautifulSoup(response.text, 'html.parser')
                        text = ""
                        for post in soup.find_all('p'):
                            text += post.get_text()

                        news = News(title=web["title"], text=text, link=web["link"], date=str(time.ctime(time.time())))
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
