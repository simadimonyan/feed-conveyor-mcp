from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.main import web

@web.tool()
def search(query) -> list[dict[str, str | None]]:
    """Search last 5 links on query"""
    driver = webdriver.Chrome()
    driver.get("https://www.google.com")

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    search_input.clear()
    search_input.send_keys(query + Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
    )

    results = []
    elems = driver.find_elements(By.CSS_SELECTOR, "h3")[:5]
    for elem in elems:
        parent = elem.find_element(By.XPATH, "..")
        results.append({
            "title": elem.text,
            "href": parent.get_attribute("href")
        })

    driver.quit()
    return results


