#! python3
#
# Here is some examples of using proca classes
# and working with production calendar data stored in JSON files


import proca
import json


# Returns dictionary loaded from JSON file
def readJSON(fileName):
    with open(fileName) as fileJSON:
        data = json.load(fileJSON)
    return data


# Construct object 2023 year production calendar
# from source JSON file
year = proca.ProcaYear(readJSON('sjob_2023_min.json'))

# Make 1st quarter months of the year
months = year(1, 2, 3, 4)

# Get January by alias 'jan'
jan = months.jan

# Print January days table
print(jan)

# Show January info using month fields
print(f'{jan.name}:',
      f'рабочих дн: {jan.twork}',
      f'выходных дн: {jan.trest}',
      f'всего дн: {jan.tdays}',
      sep='\n')

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
