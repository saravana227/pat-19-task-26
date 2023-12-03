import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IMDBSearchPage:
    def __init__(self, driver):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.search_box_locator = (By.ID, "suggestion-search")
        self.search_button_locator = (By.ID, "suggestion-search-button")
        self.sort_by_dropdown_locator = (By.ID, "sort")
        self.genre_dropdown_locator = (By.ID, "genres")

    def navigate_to_page(self):
        self.driver.get("https://www.imdb.com/search/name/")

    def fill_search_form(self, search_query, sort_by, genre):
        search_box = self.driver.find_element(*self.search_box_locator)
        search_box.send_keys(search_query)

        sort_by_dropdown = self.driver.find_element(*self.sort_by_dropdown_locator)
        sort_by_dropdown.send_keys(sort_by)

        genre_dropdown = self.driver.find_element(*self.genre_dropdown_locator)
        genre_dropdown.send_keys(genre)

    def click_search_button(self):
        search_button = self.driver.find_element(*self.search_button_locator)
        search_button.click()

class TestIMDBSearch:
    @pytest.fixture
    def setup(self):
        driver = webdriver.Firefox()
        imdb_search_page = IMDBSearchPage(driver)
        imdb_search_page.navigate_to_page()
        yield imdb_search_page
        driver.quit()

    def test_imdb_search(self, setup):
        setup.fill_search_form("Tom Hanks", "Popularity Descending", "Action")
        setup.click_search_button()

        # Explicit wait for the search results page to load
        WebDriverWait(setup.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "lister-list"))
        )

        # Add assertions or further actions as needed
        assert "Search results for" in setup.driver.title

if __name__ == "__main__":
    pytest.main()