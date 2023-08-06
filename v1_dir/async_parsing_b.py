from bs4 import BeautifulSoup
import xml.etree.ElementTree as Et 
import requests
import asyncio
import aiohttp

root = Et.Element('products')


async def get_products_data(session, page):

    url = f'https://santeh-kirov.ru/категория/ванны?PAGEN_6={page}'

    async with session.get(url=url) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "lxml")

        products = soup.find_all(class_ = 'header__menu_special-title')

        for product in products:
            if product.get('href') is not None:

                prodhtml = requests.get('https://santeh-kirov.ru/' + product.get('href')[1:]).text

                prodsoup = BeautifulSoup(prodhtml, 'lxml')

                params = prodsoup.find_all('meta')

                product_tag = Et.SubElement(root, 'product')

                # print('-' * 10) 
                #
                # print(product.text)
                # 
                # print('-' * 10)
                
                for param in params:
                    if param.get('property') is not None:
                        if 'image:' in param.get('property'):
                            pass
                            
                        elif 'og:' in param.get('property'):
                            param_tag = Et.SubElement(product_tag, param.get('property')[3:])
                            param_tag.text = param.get('content')


async def gather_data():
    
    async with aiohttp.ClientSession() as session:
        tasks = []

        for page in range(1, 12):
            task = asyncio.create_task(get_products_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())

main()
# print(ssl.get_default_verify_paths().openssl_cafile) 
Et.ElementTree(root).write('products.xml', encoding='utf-8')

