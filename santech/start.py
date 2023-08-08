import os

url = 'https://santeh-kirov.ru/категория/газовые-котлы-и-комплектующие' 

open('url.txt', 'w').write(url)

os.system('scrapy crawl santech_parser')
