import functions

# Введите название препарата
user_input = input('введите название препарата на русском языке: ').capitalize ()
letter = user_input[0].lower()

#получаем url_name препарата
url_name = functions.word_parser(letter)
#получаем name_url словарь
name_url_drug = functions.name_url_dict(url_name)
#результат парсинга и на выходе информация об искомом перпарате
res_parsing_dict = functions.res_parsing(user_input, name_url_drug)
#запись данных в файл
functions.save_file(res_parsing_dict)
