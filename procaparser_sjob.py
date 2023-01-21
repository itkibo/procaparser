#! python3
#
# procaparser_sjob.py - extracts production calendar from https://superjob.ru
# parsed result(s) is represented as a dictionary in JSON file(s)


import requests
import bs4
import json


# FUNC

# Returns dictionaries with description of days/months
def getDescription():

    dayTypes = {
        0: 'Рабочий день',
        1: 'Выходной день',
        2: 'Сокращенный день',
        3: 'Праздничный день',
    }
    dayNames = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота',
        7: 'Воскресенье',
    }
    monthNames = {
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

    return {'dtypes': dayTypes, 'dnames': dayNames, 'mnames': monthNames}


# Returns dictionary with structured month data
def extractMonthData(rows, mNum, description=getDescription()):

    monthData = {
        'name': description['mnames'][int(mNum)],
        'countdays': 0,
        'workdays': 0,
        'restdays': 0,
        'days': {},
    }

    # Iterate over rows of month block/grid
    for row in rows:

        # Get cells of a row of grid
        cells = row.select('div._1MN0y')

        # Iterate over cells in row, index is equal day of week
        for dWeek, cell in enumerate(cells, start=1):

            # Get css classes of current div element
            classes = cell.attrs['class']

            if '_2pPZd' in classes:
                # This cell is not a day of current month, skip it
                continue

            # Extract day number
            if dNum := cell.select_one("span._3d27N").string:
                try:
                    dNum = int(dNum)
                except ValueError:
                    continue

            monthData['countdays'] += 1

            # Default values of cell
            dType = 1
            dEvent = ''

            # Depends on css class chhose type of a day
            if '_1YS-8' in classes:
                # Pre holiday (light green), get event string from tooltip
                dType = 2
                dEvent = cell.select_one('div._30A54').string
                monthData['workdays'] += 1
            elif '_1c_LS' in classes:
                # Holiday/weekend (green), get event string from tooltip
                dType = 3
                dEvent = cell.select_one('div._30A54').string
                monthData['restdays'] += 1
            else:
                # This is a ordinary workday
                dType = 0
                dEvent = description['dtypes'][dType]
                monthData['workdays'] += 1

            monthData['days'][dNum] = {
                'day_num': dNum,
                'wday_num': dWeek,
                'wday_str': description['dnames'][dWeek],
                'dtype_num': dType,
                'dtype_str': dEvent,
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

basicURL = 'https://www.superjob.ru/proizvodstvennyj_kalendar'

# Iterate over pages to request (production calendar years)
for yearNum in range(2020, 2025):

    if not (pageData := requestPageData(basicURL, yearNum)):
        print('Error occured due request')
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

    if len(dctYear[yearNum]) == 0:
        print(f'Year {yearNum} skipped')
        continue

    # Saves year data into json file
    jsonData = json.dumps(dctYear, ensure_ascii=False)
    fileName = f'sjob_proca_{yearNum}.json'
    with open(fileName, "w") as outfile:
        outfile.write(jsonData)

    print(f'JSON file is ready: {fileName}')
