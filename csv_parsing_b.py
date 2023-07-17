from bs4 import BeautifulSoup
import requests
import csv

data = [
    [] 
]

category = 'мебель-для-ванной-комнаты'

def gen_attributes(params, product_num):

    param_sum = len(params)

    for i in range(1, param_sum + 1):
        if not f'Attribute {i} name' in data[0]:
            data[0].append(f'Attribute {i} name')

        if not f'Attribute {i} value(s)' in data[0]:
            data[0].append(f'Attribute {i} value(s)')

        for param in params:
            attrslist = list(param.find_all())

            if 'Артикул' in attrslist[0].text and ' ' in attrslist[0].text:
                pass

            elif 'Артикул' not in data[product_num] and attrslist[0].text == 'Артикул':
                if 'sku' not in data[0]:
                    data[0].insert(0, 'sku')

                if attrslist[1].text not in data[product_num]:
                    data[product_num].insert(0, attrslist[1].text)

            else:
                data[product_num].append(attrslist[0].text)

                data[product_num].append(attrslist[1].text)


def gen_pnid_names():
    tags = ['Visibility in catalog', 'categories', 'in stock?', 'regular price', 'name', 'images', 'description']

    for tag in tags:
        if not tag in data[0]:
            data[0].append(tag)


def gen_pnid_values(prodsoup, product_num):
    data[product_num].append(category)

    price = prodsoup.find(class_ = 'card-info__price_value')
    
    try:
        data[product_num].append(''.join([char for char in price.text if char not in '\n']).strip())

        data[product_num].insert(1, '1')
        data[product_num].insert(0, 'visible')

    except AttributeError:
        data[product_num].append('Под заказ')

        data[product_num].insert(1, '0')
        data[product_num].insert(0, 'hidden')

    prodname = prodsoup.find(class_ = 'card-info__title')
    
    data[product_num].append(''.join([char for char in prodname.text if char not in '\n']).strip())

    prodimg = prodsoup.find(class_ = 'card-img')

    data[product_num].append('https://santeh-kirov.ru' + prodimg.get('href'))

    proddesc = prodsoup.find(class_ = 'card-tabs__item_text')

    data[product_num].append(proddesc.text)


def find_pages_sum():
    ur = 'https://santeh-kirov.ru/категория/' + category

    resp = requests.get(ur).text

    bsoup = BeautifulSoup(resp, 'lxml')

    try:
        pages = bsoup.find(class_ = 'lk-notifications__pagination_items').contents

        last_page = pages[-2].text

    except:
        last_page = 1

    return int(last_page)


def main(products, product_num):
    for product in products:

        product_num += 1

        data.append(list())

        if product.get('href') is not None:

            prodhtml = requests.get('https://santeh-kirov.ru/' + product.get('href')[1:]).text

            prodsoup = BeautifulSoup(prodhtml, 'lxml')

            params = prodsoup.find_all(class_ = 'card-tabs__item_row')       

            gen_pnid_names()

            gen_pnid_values(prodsoup, product_num)
            
            gen_attributes(params, product_num)

    return product_num
 

def parse_site():
    product_num = -1

    last_page = find_pages_sum()

    for page_number in range(1, last_page + 1):

        url = f'https://santeh-kirov.ru/категория/{category}?PAGEN_6=' + str(page_number)

        response = requests.get(url)

        html = response.text

        soup = BeautifulSoup(html, 'lxml')

        products = soup.find_all(class_ = 'header__menu_special-title')

        product_num = main(products, product_num)

        print(f'{page_number}/{last_page}...')
    
    with open('products.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


parse_site()
