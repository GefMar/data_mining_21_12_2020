import requests
import bs4
from urllib.parse import urljoin
import pymongo


class MagnitParse:
    def __init__(self, start_url, mongo_db):
        self.start_url = start_url
        self.db = mongo_db
    
    def __get_soup(self, url) -> bs4.BeautifulSoup:
        # todo предусмотреть внештатные ситуации
        response = requests.get(url)
        return bs4.BeautifulSoup(response.text, 'lxml')
    
    def run(self):
        for product in self.parse():
            self.save(product)
    
    def parse(self):
        soup = self.__get_soup(self.start_url)
        catalog_main = soup.find('div', attrs={'class': 'сatalogue__main'})
        for product_tag in catalog_main.find_all('a', recursive=False):
            try:
                yield self.product_parse(product_tag)
            except AttributeError:
                pass
    
    def product_parse(self, product: bs4.Tag) -> dict:
        product = {
            'url': urljoin(self.start_url, product.get('href')),
            'name': product.find('div', attrs={'class': 'card-sale__title'}).text,
        }
        return product
    
    def save(self, data):
        collection = self.db['magnit']
        collection.insert_one(data)
        print(1)


if __name__ == '__main__':
    database = pymongo.MongoClient('mongodb://localhost:27017')['gb_parse_12']
    parser = MagnitParse("https://magnit.ru/promo/?geo=moskva", database)
    parser.run()
