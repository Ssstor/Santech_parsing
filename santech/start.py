import argparse
import os

aparser = argparse.ArgumentParser(description='Запуск парсера')
aparser.add_argument('url')

url = aparser.parse_args().url 

open(os.path.realpath(__file__).split('start.py')[0] + 'url.txt', 'w').write(url)

os.system('cd ' + os.path.realpath(__file__).split('start.py')[0] + ' && scrapy crawl santech_parser')
