from bs4 import BeautifulSoup
import requests

class Scraper():
    def __init__(self, search_term):
        self.search_term = search_term
        self.page = self.fetch_webpage()

    def fetch_webpage(self):
        """Loads results from the search_term.
        Returns the recieved request
        """
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + self.search_term
        try:
            return requests.get(url,headers=headers)
        except Exception as e:
            print(e)
            return None

    def get_title(self):
        pass

    def get_review(self):
        pass

    def get_photo(self):
        pass

    def get_price(self):
        pass

    def get_product_id(self):
        pass
