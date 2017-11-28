from bs4 import BeautifulSoup
import requests
from models import Product
from datetime import datetime

class Scraper:
    def __init__(self, search_term):
        self.search_term = search_term
        self.page = None
        self.fetch_webpage()
        self.results = None
        self.get_results()

    def fetch_webpage(self, page=1):
        """Fetches the raw webpage of product results.
        Either sets the page field to raw content or None.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&page=" + str(page) + "&field-keywords=" + self.search_term

        try:
            self.page = requests.get(url,headers=headers)
            print(self.page)

        except Exception as e:
            print(e)

    def get_results(self):
        """Fetch all of the products.
        Scrapes the webpage for the <li> elems that hold the products.
        """
        soup = BeautifulSoup(self.page.content, "html.parser")
        uls = soup.find_all("ul")
        results = []

        for ul in uls:
            lis = ul.find_all('li')

            for li in lis:
                if li.get('id'):
                    results.append(li)

        self.results = results

    def get_products(self):
        """Creates a list of products.
        Goes through every product <li> and fetches it's correct information
        by calling each individual scraping method.
        Returns a list of unique products.
        """
        products = []
        time = datetime.utcnow()

        for li in self.results:

            product = Product()
            product.keyword = self.search_term
            product.id = self.get_id(li)
            product.title = self.get_title(li)
            product.image_url = self.get_image(li)
            product.price = self.get_price(li)
            product.review = self.get_review(li)
            product.updated = time

            if not product.is_none():
                products.append(product)

        return list(set(products)) # remove any duplicate products

    def get_id(self, li):
        """Returns the product's id.
        """
        return li['data-asin']

    def get_title(self, li):
        """Returns the title of the product.
        """
        title = li.find_all('a', {"class": "a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
        return title[0].get('title') if len(title) > 0 else None

    def get_image(self, li):
        """Returns the image_url of the product.
        """
        image = str(li.find_all('img', {"class": "s-access-image cfMarker"})).split(',')[-1][1:-24]
        return image if image else None

    def get_price(self, li):
        """Returns the price of the product.
        """
        price = li.find_all('span', {"class": "sx-price sx-price-large"})

        if len(price) > 0:
            whole = price[0].find_all('span')[0].text
            fraction = price[0].find_all('sup')[1].text
            price = "$%s.%s" % (whole, fraction)

            return price

        return None

    def get_review(self, li):
        """Returns the review of the product.
        """
        review = li.find_all('span', {"class": "a-icon-alt"})
        return review[-1].text if len(review) > 0 else None

    def get_larger_image(id):
        """Returns the larger image url of a product.
        Takes in an id and scrapes it's webpage for a larger image of the product.
        Returns the larger url image.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        url = "https://www.amazon.com/dp/" + str(id)

        try:
            page = requests.get(url,headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            soup = soup.find_all("img")

            for img in soup:
                if img.get("data-old-hires"):
                    return str(img.get("data-old-hires"))

            return None

        except Exception as e:
            print(e)
            return None
