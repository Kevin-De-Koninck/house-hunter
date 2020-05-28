from logzero import logger
import requests
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
import os

class Immoweb:
    def __init__(self, settings):
        self.settings = settings
        self.base_url = "http://www.immoweb.be/en/search/{residence}/for-sale?" \
                        "countries=BE&minPrice={min_price}&maxPrice={max_price}" \
                        "&minBedroomCount={min_bedrooms}&orderBy=relevance" \
                        "&postalCodes=BE-{postal_codes}"
        
    def hello_world(self):
        data = {"min_price": 200000,
                "max_price": 300000,
                "residence": "house",
                "min_bedrooms": 2,
                "postal_codes": "%2C".join(["2630", "2200"])}
        logger.info(self.base_url.format(**data))

    def get_page(self, url=None):
        page = None
        if url is None:
            url = self.SOURCE_PAGE
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            page = requests.get(url, headers=headers)
            if page.status_code != 200:
                logger.error("Unable to retrieve page (returncode != 200):\n%s", url)
                sys.exit(1)
        except requests.exceptions.InvalidSchema as e:
            logger.error("Unable to retrieve page:\n%s", url)
            logger.exception(e)
            sys.exit(-1)
        return page

    def parse(self):
        data = {"min_price": 200000,
                "max_price": 300000,
                "residence": "house",
                "min_bedrooms": 2,
                "postal_codes": "%2C".join(["2630", "2200"])}

        display = Display(visible=0, size=(800, 600))
        display.start()

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('browser.download.folderList', 2)
        firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
        firefox_profile.set_preference('browser.download.dir', os.getcwd())
        firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        browser = webdriver.Firefox(firefox_profile=firefox_profile)

        browser.get(self.base_url.format(**data))

        soup = BeautifulSoup(browser.page_source,'html.parser')

        print(soup.find("ul", id="main-content"))


class Search_item:
    def __init__(self):
        self.url = None
        self.image = None
        self.type = None
        self.postal_code = None

