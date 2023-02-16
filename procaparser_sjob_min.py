#! python3
#
# extracts production calendar from https://superjob.ru
# parsed structured data stored in JSON file


import requests
import bs4
import json


# Returns dictionary with structured month data
def extractMonthData(rows):

    month = {}

    # Iterate over rows of month grid
    for row in rows:

        # Get cells of current row
        if not (objCells := row.select('div._1MN0y')):
            continue

        # Iterate over cells in row, index is equal dnum of week
        for dweek, cell in enumerate(objCells, start=1):

            # Get CSS classes of current div element
            classes = cell.attrs['class']

            # Cell is not a day of current month, skip it
            if '_2pPZd' in classes:
                continue

            # Extract day number
            if not (objDay := cell.select_one('span._3d27N')):
                continue

            try:
                dnum = int(objDay.string)
            except ValueError:
                continue

            ttip = ''
            # Get day short description from tooltip
            if objTTip := cell.select_one('div._30A54'):
                ttip = objTTip.string

            # day types:
            # 0 - work day, 1 - short day, 2 - weekend, 3 - holiday
            dtype = 0
            # It's pre-holiday (light green)
            if '_1YS-8' in classes:
                dtype = 1

            # Holiday or weekend (green)
            elif '_1c_LS' in classes:
                if dweek in (6, 7) and ttip == 'Выходной':
                    # Weekend
                    dtype = 2
                else:
                    # Holiday
                    dtype = 3

            month[dnum] = {
                            'dnum': dnum,
                            'dweek': dweek,
                            'dtype': dtype,
                            'ttip': ttip
                           }

    return month


# Returns page data as bs4 object
def requestPageData(baseURL, ynum):
    try:
        res = requests.get(f'{baseURL}/{ynum}/')
        res.raise_for_status()
    except Exception:
        return None

    if soup := bs4.BeautifulSoup(res.text, 'html.parser'):
        return soup
    else:
        return None


# START

basicURL = 'https://www.superjob.ru/proizvodstvennyj_kalendar'
years = '2023 2022 2021 2020'.split()

# Iterate over pages to request (production calendar years)
for ynum in years:

    if not (pageData := requestPageData(basicURL, ynum)):
        print('Error occured due request')
        continue

    year = {
        ynum: {}
    }

    mnum = 1

    for objMonthGrid in pageData.find_all('div', class_='_3O83e _3f-yB'):
        # Get month area with divs as rows
        if not (rows := objMonthGrid.select('div._1OyqE')):
            continue

        # Extract month data into dct
        if not (month := extractMonthData(rows)):
            continue

        # Collect month data into year dct
        year[ynum][mnum] = month
        mnum += 1

    if len(year[ynum]) == 0:
        print(f'Year {ynum} skipped')
        continue

    # Saves year data into JSON file
    jsonData = json.dumps(year, ensure_ascii=False)
    fileName = f'sjob_min_{ynum}.json'
    with open(fileName, "w") as outfile:
        outfile.write(jsonData)

    print(f'JSON file is ready: {fileName}')
