#! python3
#
# sjob_proca_parser.py - extracts production calendar from https://superjob.ru
# parsed result is represented as a dictionary in JSON file(s)
#
# Result dictionary structure description
# dctYear = {
#     2023: {
#         1: {
#             'name': 'Январь',
#             'total': 31,
#             'restdays': 14,
#             'workdays': 17,
#             'days': {
#                 'day_num': 1,
#                 'wday_num': 7,
#                 'wday_str': 'Воскресенье',
#                 'dtype_num': 3,
#                 'dtype_str': 'Праздничный день',
#             }
#         },
#         2: {
#             ...
#         },
#     }
# }

import requests
import bs4
import json


# FUNC

# Returns dictionary with structured month data
def extractMonthData(rows, mNum):

    dayType = {
        0: 'Рабочий день',
        1: 'Выходной день',
        2: 'Сокращенный день',
        3: 'Праздничный день',
    }

    dayWeek = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота',
        7: 'Воскресенье',
    }

    monthName = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь',
    }

    monthData = {
        'name': monthName[int(mNum)],
        'countdays': 0,
        'workdays': 0,
        'restdays': 0,
        'days': {},
    }

    # Iterate over rows of month block/grid
    for row in rows:

        cells = row.select('div._1MN0y')

        # Iterate over cells in row, index is equal day of week
        for dWeek, cell in enumerate(cells, start=1):

            # Get css classes of current div element
            classes = cell.attrs['class']

            if '_2pPZd' in classes:
                # This cell is not a day of current month, skip it
                continue

            dNum = int(cell.select_one("span._3d27N").string)
            monthData['countdays'] += 1

            # Default values of cell
            dType = 1
            dDescr = ''

            # Depends on css class set type of a day + description if exists
            if '_1YS-8' in classes:
                # Pre holiday (light green), get description from tooltip
                dType = 2
                dDescr = cell.select_one('div._30A54').string
                monthData['workdays'] += 1
            elif '_1c_LS' in classes:
                # Holiday/weekend (green), get description from tooltip
                dType = 3
                dDescr = cell.select_one('div._30A54').string
                monthData['restdays'] += 1
            else:
                # This is a ordinary workday
                dType = 0
                dDescr = dayType[dType]
                monthData['workdays'] += 1

            monthData['days'][dNum] = {
                'day_num': dNum,
                'wday_num': dWeek,
                'wday_str': dayWeek[dWeek],
                'dtype_num': dType,
                'dtype_str': dDescr,
            }

    return monthData


# Returns page data as bs4 object
def requestPageData(baseURL, yNum):

    try:
        res = requests.get(f'{baseURL}/{yNum}/')
        res.raise_for_status()
    except Exception:
        return None

    if soup := bs4.BeautifulSoup(res.text, 'html.parser'):
        return soup


# EXEC

# Iterate over pages to request (production calendar years)
for yearNum in (2023, 2022, 2021, 2020):

    if not (pageData := requestPageData('https://www.superjob.ru/proizvodstvennyj_kalendar', yearNum)):
        continue

    dctYear = {
        yearNum: {}
    }

    monthNum = 1
    for monthGrid in pageData.find_all('div', class_='_3O83e _3f-yB'):
        # Get month area with divs as rows
        rows = monthGrid.select('div._1OyqE')
        # Extract month data into dct
        dctMonth = extractMonthData(rows, monthNum)
        # Collect month data into year dct
        dctYear[yearNum][monthNum] = dctMonth
        monthNum += 1

    # Saves year data into json file
    jsonData = json.dumps(dctYear, ensure_ascii=False)
    with open(f'sjob_proca_{yearNum}.json', "w") as outfile:
        outfile.write(jsonData)
