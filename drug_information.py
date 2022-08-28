import functions
import os.path
import json

#Проверяем, что файл с именамни и ссылками есть в директории
#если нет, то делаем полный парсинг... да, долго, но что поделаешь один раз нужно будет подождать
if os.path.isfile('name_url.json'):
    #сохраняем данные название препарата - url в переменную
    with open('name_url.json', 'r', encoding = 'utf-8') as new:
        name_url_drug = json.load(new)
else:
    functions.parser_first()

# User вводит название препарата
user_input = input('введите название препарата на русском языке: ').lower()
#сохраняем первую букву
letter = user_input[0].lower()

#проверяем, что препарат есть в списке 
if user_input in name_url_drug:
    #проверяем препарат в базе. Если есть, то вытвскиваем инфу оттуда
    if bool(functions.look_at_my_data(user_input)):
        #информация об искомом перпарате из своей базы данных
        res_parsing_dict = functions.look_at_my_data(user_input)
        functions.save_file(res_parsing_dict)
    else:
        res_parsing_dict = functions.res_parsing(user_input, name_url_drug)
        functions.save_file(res_parsing_dict)
        #добавляем в базу данных
        functions.data_to_the_database()
#если нет в списке, то проводим отедльный парсинг с сайта vidal.ru
else:
    #получаем url_name препарата
    url_name = functions.word_parser(letter)
    #получаем name_url словарь
    name_url_drug = functions.name_url_dict(url_name)
    #результат парсинга и на выходе информация об искомом перпарате
    res_parsing_dict = functions.res_parsing(user_input, name_url_drug)
    #запись данных в файл
    functions.save_file(res_parsing_dict)
    #добавляем в базу данных
    functions.data_to_the_database()

#Вывод информации
with open('medicine.json', 'r', encoding='utf-8') as f:
    text = json.load(f)

for key, value in text.items():
    print(f'{key} : {value}')