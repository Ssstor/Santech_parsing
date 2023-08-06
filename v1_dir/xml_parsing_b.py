from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import xml.etree.ElementTree as Et 
import requests

root = Et.Element('products')


def parse_site():
    for page_number in range(1, 12):

        url = 'https://santeh-kirov.ru/категория/ванны?PAGEN_6=' + str(page_number)

        response = requests.get(url)

        html = response.text

        soup = BeautifulSoup(html, 'lxml')

        products = soup.find_all(class_ = 'header__menu_special-title')

        for product in products:    
            if product.get('href') is not None:

                prodhtml = requests.get('https://santeh-kirov.ru/' + product.get('href')[1:]).text

                prodsoup = BeautifulSoup(prodhtml, 'lxml')

                params = prodsoup.find_all(class_ = 'card-info__table_row')

                product_tag = Et.SubElement(root, 'product')

                # print(product.text)
                #
                # print('-' * 10)
                 
                for param in params:
                    paramslist = list(param.find_all())

                    tag_name = GoogleTranslator(source='ru', target='en').translate(paramslist[0].text).replace(' ', '_')

                    if len(paramslist) != 2:
                        pass

                    elif tag_name == 'vendor_code':
                        pass

                    elif ':' in tag_name:
                        tag_name = ''.join([char for char in tag_name if char not in ':'])
                        
                        param_tag = Et.SubElement(product_tag, tag_name)
                        param_tag.text = paramslist[1].text

                        print(tag_name)

                        # break
                    else:
                        param_tag = Et.SubElement(product_tag, tag_name)
                        param_tag.text = paramslist[1].text

                        print(tag_name)


        # print(page_number)
    Et.ElementTree(root).write('products.xml', encoding='utf-8')


parse_site()


# url = 'https://santeh-kirov.ru/product/16147/'
#
# response = requests.get(url)
#
# html = response.text
#
# open('page_source.html', 'w').write(html)
