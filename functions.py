import json
import requests
from bs4 import BeautifulSoup
import time

url = 'https://www.vidal.ru/'


#парсер всех страниц по искомой букве
def word_parser(letter):

    alphabet = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e',
            'ж':'zh','з':'z','и':'i','й':'j','к':'k','л':'l',
            'м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t',
            'у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','э':'eh','ю':'yu','я':'ya'}

    url_lek = 'drugs/products/p/rus-'
    param = '?p='
    letter = alphabet[letter]
    page = 1
    url_name = []

    while True:
        print(f'страница: {page}')
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
            break
        time.sleep(1)
    
    return url_name

#формируем словарь name - url
def name_url_dict(url_name):
    name_url_drug = {}

    for i in range(len(url_name)):
        name_url_drug[url_name[i][1]] = url_name[i][0]
    
    return name_url_drug

#формируем окончательные результаты: фармгруппа, Производитель, Форма препарата, Для чего применять, Режим дозирования, Противопоказания:
def res_parsing(user_input, name_url_drug):
    res_parsing_dict = {}
    #делаем реквест искомого препарата
    url_drug = name_url_drug[user_input]
    response = requests.get(url+url_drug)
    soup = BeautifulSoup(response.text, 'html.parser')

    res_pharm_group = soup.find_all('span', class_= ['block-content','no-underline'])
    res_dosage_form = soup.find_all('td', class_= 'products-table-zip')
    res_for_what = soup.find_all('div', class_= ['block-content','no-underline'])
    res_manufacturer = soup.find_all('a', class_= ['block-head','no-underline'])

    res_parsing_dict['название препарата'] = user_input
    res_parsing_dict['фарм группа'] = res_pharm_group[2].text.replace('\n', '').strip()
    res_parsing_dict['произволитель'] = res_manufacturer[1].text.replace('\n', '').strip()
    res_parsing_dict['форма выпуска'] = res_dosage_form[0].text.split('№')[0].replace('\n', '').strip()
    res_parsing_dict['показания к применению'] = res_for_what[4].text.replace('\n', '').strip()
    res_parsing_dict['режим дозирования'] = res_for_what[6].text.replace('\n', '').strip()
    res_parsing_dict['противопоказания'] = res_for_what[8].text.replace('\n', '').strip()

    return res_parsing_dict

#Записываем в файл результаты
def save_file(res_parsing_dict):
    with open("medicine.json", "w") as write_file:
        json.dump(res_parsing_dict, write_file, ensure_ascii=False)