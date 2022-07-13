import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from sheets_api import write_data

count = 1
driver = webdriver.Chrome()
driver.get('https://karusel.ru/catalog/')
driver.find_elements(By.TAG_NAME, 'button')[3].click()
catalog = driver.find_element(By.CLASS_NAME, 'promo-catalog-menu-list__container').get_attribute('innerHTML')
driver.close()
categories = BeautifulSoup(catalog, 'lxml').find_all('li')
catalogs_count = 0
products_count = 0
product_list = []

for category in categories:
    catalogs_count += 1
    products = []
    response = requests.get('https://karusel.ru' + category.a.get('href'))
    ul_subcategories = BeautifulSoup(response.content, 'lxml').find(
        'ul', {'class':'promo-catalog-menu-list__container promo-catalog-menu-list__sub'})
    li_subcategories = ul_subcategories.find_all('li')
    for li_subcategory in li_subcategories:
        subcategory_name = li_subcategory.a.text
        row_subcategory = requests.get('https://karusel.ru' + li_subcategory.a.get('href')).content
        subcategory = BeautifulSoup(row_subcategory, 'lxml')
        promo_class = 'card card--none promo-catalog-product promo-catalog-product--hammer card--with-hover card--fit-content'
        standart_class = 'card card--none promo-catalog-product card--with-hover card--fit-content'
        products += subcategory.find_all('div', {'class':promo_class})
        products += subcategory.find_all('div', {'class':standart_class})
        for product in products:
            product_name = product.find('div',{'class':'promo-catalog-product__name'}).text
            product_price = product.find('div',{'class':'promo-catalog-product__price'}).text.split()[0]
            product_list.append([subcategory_name, product_name, product_price])
            print(product_list[len(product_list)-1])
            products_count += 1
            if len(product_list)>15:
                write_data(product_list, count)
                count += len(product_list)
                product_list = []
                print(products_count)

        time.sleep(8)
    time.sleep(100)

print(catalogs_count)








