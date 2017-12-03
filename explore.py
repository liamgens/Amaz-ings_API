from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from time import sleep
from models import Product
from collections import OrderedDict

def get_page_content(url):

    try:
        driver = webdriver.Firefox()
        driver.get(url)

        images = []
        results = []

        driver.execute_script("document.getElementById('nav-tools').remove()")



        results.extend(driver.find_elements_by_class_name('s-item-container'))

        n = len(results)
        i = 0
        while i < n:
            sleep(2)
            result = results[i]

            if result.size.get('width') == results[0].size.get('width'):
                result.click()

                sleep(1)
                close = driver.find_elements_by_class_name('a-button-close')

                if close:
                    close[1].click()

            results.extend(driver.find_elements_by_class_name('s-item-container'))
            results = list(OrderedDict.fromkeys(results))
            n = len(results)
            i+= 1



        driver.quit()

        return images

    except Exception as e:
        print("error:", e)
        # driver.quit()

def get_products(page_content):
    soup = BeautifulSoup(page_content, "html.parser")
    product_divs = soup.findAll("li", {"class":"s-result-item"})
    images = []

    for product in product_divs:
        images.extend(product.findAll("img", {"class": "s-access-image"}))

    for i in range(0, len(images)):
        image = images[i].get('src').split('.')
        image[3] = "_AC_SR1000,1500_"
        image = ".".join(image)
        images[i] = image

    return images

content = get_page_content("https://www.amazon.com/stream")
# for i in content:
#     print(i, '\n')
# print (len(content))
