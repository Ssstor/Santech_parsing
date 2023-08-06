import scrapy


class SantechParserSpider(scrapy.Spider):
    name = "santech_parser"
    allowed_domains = ["santeh-kirov.ru"]
    start_urls = ["https://santeh-kirov.ru/"]

    def parse(self, response):
        pass
