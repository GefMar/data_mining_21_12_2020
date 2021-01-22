import os
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.spiders.autoyoula import AutoyoulaSpider
from gb_parse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    load_dotenv('.env')
    tasks = []
    crawler_settings = Settings()
    crawler_settings.setmodule('gb_parse.settings')
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(InstagramSpider, login=os.getenv('LOGIN'), password=os.getenv('ENC_PASSWORD'), tag_list=['python', 'питер', 'программирование'])
    crawler_process.start()
