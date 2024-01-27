from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Scraper.Scraper import settings as my_settings
from Scraper.Scraper.spiders.lessons import LessonsSpider
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('Grupa', type=str)
parser.add_argument('Semestr', type=str)

args = parser.parse_args()
crawler_settings = Settings()
crawler_settings.setmodule(my_settings)
process = CrawlerProcess(settings=crawler_settings)

process.crawl(LessonsSpider, start_urls= [f'https://old.wcy.wat.edu.pl/pl/rozklad?grupa_id={args.Grupa}'], group=f'{args.Grupa}', sem=f'{args.Semestr}')
process.start()

