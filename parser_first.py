
import json
import requests
from bs4 import BeautifulSoup
import time
import classes_ORM

def parser_first():
    url = 'https://www.vidal.ru/'
    url_lek = 'drugs/products/p/rus-'
    param = '?p='
    page = 1
    alphabet = ['a','b','v','g','d','e',
                'zh','z','i','j','k','l',
                'm','n','o','p','r','s','t',
                'u','f','h','ts','ch','sh','eh','yu','ya']
    alphabet_num = 0
    url_name = []

    while True:
        if alphabet_num <= 2:
            letter = alphabet[alphabet_num] 
            res = url+url_lek+letter+param+str(page)
            response = requests.get(res)
            soup = BeautifulSoup(response.text, 'html.parser')
            res_soup = soup.find_all('td', class_=['products-table-name','no-underline'])
            try:
                res_soup[0].text
                #формируем список url - name препарата
                for i in range(len(res_soup)):
                    res = str(res_soup[i]).replace('<td class="products-table-name">\n<a class="no-underline" href="','').replace('">\n                ','&&&').replace('\n            </a>\n</td>','').replace('<sup>®</sup>\n</a>\n</td>', '').replace('<sup>®</sup>','')
                    res = res.split('&&&')
                    url_name.append(res)
                page += 1     
            except IndexError:
                print('Error')
                alphabet_num += 1
                page = 1
        else:
            break
        #включить если банят
        # time.sleep(1)

    #формируем словарь name - url
    name_url_drug = {}

    for i in range(len(url_name)):
            name_url_drug[url_name[i][1]] = url_name[i][0]

    #сохраняем json файл
    with open("name_url.json", "w", encoding='utf-8') as write_file:
            json.dump(name_url_drug, write_file)

    return f'Новый парсинг с сайта завершен. Файл name_url.json создан'        