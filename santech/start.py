import os

url = 'https://santeh-kirov.ru/категория/газовые-котлы-и-комплектующие' 

open(os.path.realpath(__file__).split('start.py')[0] + 'url.txt', 'w').write(url)

os.system('cd ' + os.path.realpath(__file__).split('start.py')[0] + ' && scrapy crawl santech_parser')
