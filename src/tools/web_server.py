from mcp.server import FastMCP
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class WebTools:

    def __init__(self, web: FastMCP):
        self.web = web

        web.tool(
            name="mcp_search",
            description="Ищет 5 первых ссылок в Google. Нельзя указывать в запросе больше 5 слов",
        ) (self.search)

    @staticmethod
    def search(query: str) -> list[dict[str, str | None]]:
        """Search last 5 links on query"""

        results = []

        try:

            service = Service()
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            driver = webdriver.Firefox(service=service, options=options)

            driver.get("https://www.google.com")

            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )

            search_input.clear()
            search_input.send_keys(query + Keys.RETURN)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
            )

            elems = driver.find_elements(By.CSS_SELECTOR, "h3")[:5]
            for elem in elems:
                parent = elem.find_element(By.XPATH, "..")
                results.append({
                    "title": elem.text,
                    "href": parent.get_attribute("href")
                })
                print("\n")
                print(results)
                print("\n")

            driver.quit()

        except Exception as e:
            print("\n")
            print(e)
            print("\n")

        return results
