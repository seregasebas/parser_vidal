import json
import requests
from bs4 import BeautifulSoup
import time
import classes_ORM

url = 'https://www.vidal.ru/'

#парсер для создания файла name_url.json название препарата - ссылка
def parser_first():
    '''Данный парсер создает файл название препарата-ссылка для всех страниц сайта vidal.ru
       Его запускать только при первой работе с программой или для обновления файла name_url.json'''
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
        if alphabet_num < len(alphabet):
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
                #следующая буква
                alphabet_num += 1
                #возвращаем на первую страницу
                page = 1
        else:
            break
        # #включить если банят
        # time.sleep(1)

    #формируем словарь name - url
    name_url_drug = {}

    for i in range(len(url_name)):
            name_url_drug[url_name[i][1].lower()] = url_name[i][0]

    #сохраняем json файл
    with open("name_url.json", "w", encoding='utf-8') as write_file:
            json.dump(name_url_drug, write_file)

    return f'Новый парсинг с сайта завершен. Файл name_url.json создан'

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
    res_parsing_dict['производитель'] = res_manufacturer[1].text.replace('\n', '').strip()
    res_parsing_dict['форма выпуска'] = res_dosage_form[0].text.split('№')[0].replace('\n', '').strip()
    res_parsing_dict['показания к применению'] = res_for_what[4].text.replace('\n', '').strip()
    res_parsing_dict['режим дозирования'] = res_for_what[6].text.replace('\n', '').strip()
    res_parsing_dict['противопоказания'] = res_for_what[8].text.replace('\n', '').strip()

    return res_parsing_dict

#Записываем в файл результаты
def save_file(res_parsing_dict):
    with open("medicine.json", "w") as write_file:
        json.dump(res_parsing_dict, write_file, ensure_ascii=False)


#TODO: сделать через ORM
#функция внесения нужной информации в базу данных
def data_to_the_database():
    #присваиваем переменной название препарата 
    name_query = classes_ORM.session.query(classes_ORM.Drug_info).all()
     #формируем список имен
    name = []
    for i in name_query:
        name.append(i.name)
    name = set(name)
    #открываем json файл с данными парсинга
    with open('medicine.json', 'r', encoding='utf-8') as f: #открыли файл с данными
        text = json.load(f) #загнали все, что получилось в переменную
    #присваиваем значения к нужным переменным
    name_drug = text['название препарата']
    pharm_group = text['фарм группа']
    manufacturer = text['производитель']
    form = text['форма выпуска']
    indications = text['показания к применению']
    doses = text['режим дозирования']
    contraindications = text['противопоказания']

    #Сначала вносим данные в таблицы с вакансиями, городами и скиллами. Если такие уже есть, данные не вносятся.
    if name_drug not in name:
        res = classes_ORM.Drug_info(name_drug, pharm_group, manufacturer, form, indications, doses, contraindications)
        classes_ORM.session.add(res)
    else:
        pass
    #коммитим данные
    classes_ORM.session.commit()

#функция получения нужной информации из существующей базы данных
def look_at_my_data(user_input):
    #Вытыскмваем id добавленных или уже существующих значений города и вакансии, полученных с очередного парсинга
    data = classes_ORM.session.query(classes_ORM.Drug_info).filter(classes_ORM.Drug_info.name == user_input).all()

    res = {}
    for i in data:
        res['название препарата'] = (i.name)
        res['фарм группа'] = (i.pharm_group)
        res['производитель'] = (i.manufacturer)
        res['форма выпуска'] = (i.form)
        res['показания к применению'] = (i.indications)
        res['режим дозирования'] = (i.doses)
        res['противопоказания'] = (i.contraindications)

    return res