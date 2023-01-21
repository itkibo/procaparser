#! python3
#
# Here is some examples of working with production calendar JSON files
# with using proca module


import proca
import json


# Returns dictionary loaded from JSON file
def readJSON(fileName):
    with open(fileName) as fileJSON:
        data = json.load(fileJSON)
    return data


# Construct object 2023 year production calendar
# from source JSON file
year = proca.ProcaYear(readJSON('sjob_proca_2023.json'))
print(f'Год: {year.year_num}')

# Get thirst month of a year
january = year.getMonth(1)

# These all the same result
january = year.getMonth(1)
january = year.getMonth('1')

# Get the same result using select method
january = year.select(1)
january = year.select('1')

# Show January info
print(
    f'{january.mon_name}\n'
    f'{january.days_total} - всего дней\n'
    f'{january.days_rest} - выходных/праздничных\n'
    f'{january.days_work} - рабочих\n'
    )

# Print days in human readable table
january.printMe()
# Print days with format
january.printMe(
        {'day_num': 5, 'wday_str': 12, 'dtype_str': 40},
        gap='-',
        hide=True
    )

# Days property contains dictionary with all days
days = january.days
print(days)

# Get 31 day of January, it's dictionary
day = january.getDay(31)

# These all the same result
day = january.getDay('31')

# Get same day using 'month.day' format
day = year.select(1.31)
day = year.select('1.31')
day = year.select('01.31')

# Print day dictionary as is
print(day)
# Print day dictionary more readable
print(*[str(f'{k}: {v}') for k, v in year.select('01.07').items()], sep='\n')

# Is it rest day?
print(f'7 Января праздничный: {january.isRest(7)}')
# Is it work day?
print(f'31 Января рабочий: {january.isWork(31)}')
# Print only non-workable days in January
print(*[
    f'{str(dNum).rjust(2, "0")} {january.mon_name[0:3]} {year.year_num}г. - выходной'
    for dNum in range(1, len(january.days) + 2) if january.isRest(dNum)
    ], sep='\n')

# Print all months of year as table
year.printMe()

# Count total days in year
print(f'Дней в году: {sum([year.getMonth(mNum).days_total for mNum in range(1, 13)])}')

# Print all holidays/weekends + count total non-work days
totRest = 0
mList = [year.getMonth(mNum) for mNum in range(1, 13)]
for month in mList:
    print(f'{month.mon_name}')
    print(f'Празничные и выходные: {month.days_rest} дн.')
    for dNum in range(0, len(month.days) + 1):
        if month.isRest(dNum):
            day = month.getDay(dNum)
            totRest += 1
            print(
                f'{str(year.year_num)}.{str(month.mon_num).rjust(2, "0")}.{str(day["day_num"]).rjust(2, "0")}',
                f'{day["wday_str"].ljust(12)}',
                f'{day["dtype_str"]}',
                sep=' '
                )

    print(f'{"-"*72}')

print(f'Всего нерабочих дней: {totRest}')



import proca
import json

# Construct object 2023 year production calendar
# from source JSON file using ProcaYear
year = proca.ProcaYear(readJSON('sjob_proca_2023.json'))

# Get month January
january = year.getMonth(1)
# Print some January info
print(f'Выходных: {january.days_total}, рабочих дней: {january.days_work}')

# Is 7 of January is rest day?
print(january.isRest(7))
# Is work day?
print(january.isWork(31))

# Get day 7 of January
day7 = january.getDay(7)
# Same result by using selector format month.day
day7 = year.select(1.7)
# It' the same
day7 = year.select('01.07')

# What is weekday of 7 of January?
print(day7['wday_str'])

# Print all days of January with formatted table
# field_name: column_width
january.printMe(
    {'day_num': 5, 'wday_str': 12, 'dtype_str': 40},
    gap='-',
    hide=True
)
