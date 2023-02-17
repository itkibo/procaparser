# procaparser.py
Extracts production calendar from https://superjob.ru  
Parsed result is represented as a dictionary and stored JSON file(s)  

Парсит производственный календарь разных лет с сайта https://superjob.ru  
Результат сохраняет структурой словаря в JSON файл(ы)

## Example of result dictionary structure

```python
{
  '2023':
      {
       '1': {
              '1': {
                     'dnum': 1,
                     'dweek': 7,
                     'dtype': 3,
                     'ttip': 'Праздничный день. Новогодние каникулы'
                    },
               '2': {
                     ...  # next day
                    },
            
            },
       '2': {
             ...  # next month
            },
       }
}
```
# proca.py module
Contains proca classes for working with production calendar data  
proca builds objects of a calendar based on dictionary data  
such data in JSON files may be parsed and prepared with procaparser  
or just get ready JSON files from this repository  

Содержит proca классы для работы с производственными календарями  
proca создает объекты календарей на основе словаря с данными  
такие данные в JSON формате могут быть спарсены при помощи procaparser  
или есть уже готовые JSON файлы данных в этом репозитория  

# proca_examples.py
Same python3 code examples of using proca is in proca_examples.py  
Примеры python кода в файле proca_examples.py  

## Examples of using proca classes over JSON file (2023 prod calendar data)

```python
import proca
import json


# Returns dictionary loaded from JSON file
def readJSON(fileName):
    with open(fileName) as fileJSON:
        data = json.load(fileJSON)
    return data


# Construct object 2023 year production calendar
# from source JSON file
year = proca.ProcaYear(readJSON('sjob_min_2023.json'))

# Make 1st quarter months of the year
months = year(1, 2, 3, 4)

# Get January by alias 'jan'
jan = months.jan

# Print January days table
print(jan)
```

```
2023.01.01 | 7 Воскресенье | 3 Праздничный день. Новогодние каникулы
2023.01.02 | 1 Понедельник | 3 Праздничный день
2023.01.03 | 2 Вторник     | 3 Праздничный день
2023.01.04 | 3 Среда       | 3 Праздничный день
2023.01.05 | 4 Четверг     | 3 Праздничный день
2023.01.06 | 5 Пятница     | 3 Праздничный день
2023.01.07 | 6 Суббота     | 3 Праздничный день. Рождество Христово
2023.01.08 | 7 Воскресенье | 3 Праздничный день
2023.01.09 | 1 Понедельник | 0 Рабочий
2023.01.10 | 2 Вторник     | 0 Рабочий
2023.01.11 | 3 Среда       | 0 Рабочий
2023.01.12 | 4 Четверг     | 0 Рабочий
2023.01.13 | 5 Пятница     | 0 Рабочий
2023.01.14 | 6 Суббота     | 2 Выходной
2023.01.15 | 7 Воскресенье | 2 Выходной
2023.01.16 | 1 Понедельник | 0 Рабочий
2023.01.17 | 2 Вторник     | 0 Рабочий
2023.01.18 | 3 Среда       | 0 Рабочий
2023.01.19 | 4 Четверг     | 0 Рабочий
2023.01.20 | 5 Пятница     | 0 Рабочий
2023.01.21 | 6 Суббота     | 2 Выходной
2023.01.22 | 7 Воскресенье | 2 Выходной
2023.01.23 | 1 Понедельник | 0 Рабочий
2023.01.24 | 2 Вторник     | 0 Рабочий
2023.01.25 | 3 Среда       | 0 Рабочий
2023.01.26 | 4 Четверг     | 0 Рабочий
2023.01.27 | 5 Пятница     | 0 Рабочий
2023.01.28 | 6 Суббота     | 2 Выходной
2023.01.29 | 7 Воскресенье | 2 Выходной
2023.01.30 | 1 Понедельник | 0 Рабочий
2023.01.31 | 2 Вторник     | 0 Рабочий
```
```python
# Show January info using month fields
print(f'{jan.name}:',
      f'рабочих дн: {jan.twork}',
      f'выходных дн: {jan.trest}',
      f'всего дн: {jan.tdays}',
      sep='\n')
```
```
Январь:
рабочих дн: 17
выходных дн: 14
всего дн: 31
```
```python
# Get 7th day of January by alias 'd7'
d7 = jan.days.d7

# Print day info table
print(d7)

# Show day info using day fields
print(f'дата: {d7.dnum:02d}.{d7.mnum:02d}.{d7.ynum}',
      f'день недели: {d7.name}',
      f'выходной день: {"Да" if d7.rest == 1 else "Нет"}',
      f'праздник: {d7.ttip if d7.dtype == 3 else "Нет"}',
      sep='\n')
```
```
2023.01.07 | 6 Суббота     | 3 Праздничный день. Рождество Христово

дата: 07.01.2023
день недели: Суббота
выходной день: Да
праздник: Праздничный день. Рождество Христово
```
```python
# Make 12 months (it's default if not args passed)
months = year()

# Table header
stick = ' | '
fields_width = {'mnum': 2, 'name': 8, 'tdays': 4, 'twork': 4, 'trest': 4}
fields_ru = {'mnum': '#', 'name': 'мес.', 'tdays': 'дн.',
             'twork': 'раб.', 'trest': 'вых.'}

# Show table header
print(*[fields_ru[f].ljust(w) for f, w in fields_width.items()], sep=stick)

# Show top line
print('-' * (sum(fields_width.values()) + len(stick)*4))

# Show months info table
for m in months:
    row = []
    for f, w in fields_width.items():
        if f == 'mnum':
            # 2 pos digit with leading zero
            cell = f'{getattr(m, f):02d}'.rjust(w)
        else:
            cell = str(getattr(m, f)).ljust(w)
        row.append(cell)
    print(*row, sep=stick)

# Show bottom line
print('-' * (sum(fields_width.values()) + len(stick)*4))

# Calculate totals by 12 months
fields_total = ('tdays', 'twork', 'trest')
totals = {f: sum(getattr(m, f, 0) for m in months) for f in fields_total}
# Show table totals
print(*[str(totals[f]).ljust(w)
        if f in fields_total
        else ''.ljust(w)
        for f, w in fields_width.items()], sep=' | ')
```
```
#  | мес.     | дн.  | раб. | вых.
----------------------------------
01 | Январь   | 31   | 17   | 14  
02 | Февраль  | 28   | 18   | 10  
03 | Март     | 31   | 22   | 9   
04 | Апрель   | 30   | 20   | 10  
05 | Май      | 31   | 20   | 11  
06 | Июнь     | 30   | 21   | 9   
07 | Июль     | 31   | 21   | 10  
08 | Август   | 31   | 23   | 8   
09 | Сентябрь | 30   | 21   | 9   
10 | Октябрь  | 31   | 22   | 9   
11 | Ноябрь   | 30   | 21   | 9   
12 | Декабрь  | 31   | 21   | 10  
----------------------------------
   |          | 365  | 247  | 118 
```
