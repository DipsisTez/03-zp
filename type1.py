import csv
from datetime import datetime

def read_csv(filename):
    table = {}
    # Открываем файл
    with open(filename, encoding='utf-8') as csvfile:
        # Читаем CSV файл с указанием разделителя и символа кавычек
        spam = csv.reader(csvfile, delimiter=',', quotechar='"')
        # Получаем заголовки из первой строки
        headers = next(spam)
        # Заполняем словарь данными
        for row in spam:
            for header, value in zip(headers, row):
                if header not in table:
                    table[header] = []
                table[header].append(value)
    return table

def create_rows(table):
    headers = list(table.keys())
    return [dict(zip(headers, [table[header][i] for header in headers])) for i in range(len(table[headers[0]]))]


# Функция для преобразования строки в дату
def str_to_date(date_str):
    return datetime.strptime(date_str, '%m/%d/%Y')


rows1 = create_rows(read_csv('03-1.csv'))
rows2 = create_rows(read_csv('03-2.csv'))
rows3 = create_rows(read_csv('03-3.csv'))

shops = [row for row in rows3 if row["Район"] == 'Первомайский']
items = [row for row in rows2 if row["Наименование товара"] == 'Крупа манная']

drivers = [row for row in rows1 if row["Артикул"] in [item['Артикул'] for item in items] and row["ID магазина"] in [shop["ID магазина"] for shop in shops]]


# Отфильтровываем данные по дате
filtered_drivers = [row for row in drivers if str_to_date(row['Дата']) >= str_to_date('06/01/2021') and str_to_date(row['Дата']) <= str_to_date('06/10/2021')]

# Сортируем данные по дате
sorted_drivers = sorted(filtered_drivers, key=lambda row: str_to_date(row['Дата']))

summary = 0

for i in sorted_drivers:
	s = int(i['Количество упаковок, шт.'])
	
	if i['Тип операции']=='Поступление':
		summary += s
	else:
		summary -= s	
	

print(summary)
