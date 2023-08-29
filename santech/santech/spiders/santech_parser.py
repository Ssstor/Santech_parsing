from woocommerce import API
import scrapy


wcm = API(    
    url='https://sanstart.ru',
    consumer_key='ck_0a4297e6093ee5a75df83a36f82d5c2e7bfbab0c',
    consumer_secret='cs_b46226294c404f7d4fd53b83f50d7c0d827e0816',
    version='wc/v3'
)

class SantechParserSpider(scrapy.Spider):
    name = 'santech_parser'
    allowed_domains = ['santeh-kirov.ru']
    start_urls = ['https://santeh-kirov.ru/']
    url = open('url.txt', 'r').read().strip()  # 'https://santeh-kirov.ru/категория/газовые-котлы-и-комплектующие'
    pages_count = 1
    # useragent = UserAgent()
    custom_settings = {
        'FEEDS': { 'products.csv': { 'format': 'csv', 'overwrite': True}}
    }
    attributes_count = 0
    categories = wcm.get('products/categories').json()
    root_category = url.split('https://santeh-kirov.ru/категория/')[-1].replace('-', ' ').capitalize()


    

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse_pages_count)


    def parse_pages_count(self, response):
        try:
            self.pages_count = int(response.xpath('//div[@class = "lk-notifications__pagination_items"]/a/text()').extract()[-1])
    
        except:
            pass

        for page in range(1, self.pages_count + 1):
            url = f'{self.url}?PAGEN_6={page}'
            yield scrapy.Request(url, callback=self.parse_url)


    def parse_url(self, response, **kwargs):
        for href in response.xpath('//a[@class = "header__menu_special-title"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        category_id = None
        category_name = response.xpath('//span[@itemprop = "name"]/text()').extract()[-2]

        wcm = API(    
            url='https://sanstart.ru',
            consumer_key='ck_0a4297e6093ee5a75df83a36f82d5c2e7bfbab0c',
            consumer_secret='cs_b46226294c404f7d4fd53b83f50d7c0d827e0816',
            version='wc/v3'
        )

        for category in self.categories:
            if category['name'] == category_name:
                category_id = category['id']
                break

        if category_id == None:
            root_category_id = None

            for category in self.categories:
                if category['name'] == self.root_category:
                    root_category_id = category['id']
                    break


            new_category_data = {
                'name': category_name,
                'parent': root_category_id

            }

            wcm.post('products/categories', new_category_data).json()

            categories = wcm.get('products/categories').json()

            for category in categories:
                if category['name'] == category_name:
                    category_id = category['id']
                    break

        try:
            item = {
                'test': self.categories[0],
                'sku': response.xpath('//div[@class = "card-tabs__item_row"]/div[2]/text()').extract()[0],
                'name': response.xpath('//h1[@class = "card-info__title"]/text()').extract_first('').strip(),
                'categories': [{'id': category_id}],
                'images': [{'src': 'https://santeh-kirov.ru' + response.xpath('//a[@class = "card-img"]/@href').extract()[0]}],
                'description': response.xpath('//div[@class = "card-tabs__item_text "]/text()').extract()[0].strip(),
                'Visibility in catalog': 'visible',
                'regular price': response.xpath('//div[@class = "card-info__price_value"]/text()').extract()[0].strip(),
            }

        except:
            item = {
                'sku': response.xpath('//div[@class = "card-tabs__item_row"]/div[2]/text()').extract()[0],
                'name': response.xpath('//h1[@class = "card-info__title"]/text()').extract_first('').strip(),
                'categories': [{'id': category_id}],
                'images': [{'src': 'https://santeh-kirov.ru' + response.xpath('//a[@class = "card-img"]/@href').extract()[0]}],
                'description': response.xpath('//div[@class = "card-tabs__item_text "]/text()').extract()[0].strip(),
                'Visibility in catalog': 'hidden',
                'regular price': 'Под заказ',

            }

        if 'нет' in response.xpath('//div[@class = "card-info__table_col"]/text()').extract()[-2].strip():
            item['In stock?'] = '2'

        else:
            item['In stock?'] = '1'
        
        attribute_names = response.xpath('//div[@class = "card-tabs__item_table"]/div/div[1]/text()').extract()

        for attribute_name in attribute_names:
            attribute_num = attribute_names.index(attribute_name) + 1 
            item[f'Attribute {attribute_num} name'] = attribute_name


        attribute_values = response.xpath('//div[@class = "card-tabs__item_table"]/div/div[2]/text()').extract()

        for attribute_value in attribute_values:
            attribute_num = attribute_values.index(attribute_value) + 1

            item[f'Attribute {attribute_num} value(s)'] = attribute_value        
        
        wcm.post('products', item).json()

        yield item
 
