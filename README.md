# 03-zp

## Описание
Этот код предназначен для чтения и обработки данных из CSV-файлов. Он читает данные из трех CSV-файлов, фильтрует их по определенным критериям, затем сортирует и вычисляет сумму продаж.

## Код
```python
import csv
from datetime import datetime

# Функция для чтения CSV файла
def read_csv(filename):
    """
    Эта функция читает данные из CSV файла и возвращает их в виде словаря.
    Ключами словаря являются заголовки столбцов, а значениями - списки данных в этих столбцах.
    """
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

# Функция для создания строк из таблицы
def create_rows(table):
    """
    Эта функция преобразует таблицу (словарь списков) в список словарей.
    Каждый словарь представляет собой строку таблицы.
    """
    headers = list(table.keys())
    return [dict(zip(headers, [table[header][i] for header in headers])) for i in range(len(table[headers[0]]))]

# Функция для преобразования строки в дату
def str_to_date(date_str):
    """
    Эта функция преобразует строку в объект datetime.
    """
    return datetime.strptime(date_str, '%m/%d/%Y')

# Читаем CSV файлы и создаем строки из таблиц
rows1 = create_rows(read_csv('03-1.csv'))
rows2 = create_rows(read_csv('03-2.csv'))
rows3 = create_rows(read_csv('03-3.csv'))

# Фильтруем данные по району и поставщику
shops = [row for row in rows3 if row["Район"] == 'Октябрьский']
items = [row for row in rows2 if row["Поставщик"] == 'Экопродукты']

# Фильтруем данные по артикулу и ID магазина
drivers = [row for row in rows1 if row["Артикул"] in [item['Артикул'] for item in items] and row["ID магазина"] in [shop["ID магазина"] for shop in shops]]

# Отфильтровываем данные по дате
filtered_drivers = [row for row in drivers if str_to_date(row['Дата']) >= str_to_date('06/01/2021') and str_to_date(row['Дата']) <= str_to_date('06/10/2021')]

# Сортируем данные по дате
sorted_drivers = sorted(filtered_drivers, key=lambda row: str_to_date(row['Дата']))

summary = 0

# Вычисляем сумму продаж
for i in sorted_drivers:
    s = int(i['Цена руб./шт.'])
    t = int(i['Количество упаковок, шт.'])
    
    if i['Тип операции']!='Поступление':
        summary += s*t
    
print(summary)
```
