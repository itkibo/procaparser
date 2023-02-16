#! python3
#
# proca classes is for working with production calendar data
# it helps to work with months and days using objects approach
# proca builds objects of a calendar based on dictionary data
# such data in JSON files may be parsed and prepared with procaparser

from collections import namedtuple
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class ProcaDay:
    '''Class to store day info'''

    dnum: int  # day number
    dweek: int  # number of weekday
    dtype: int  # day type
    ttip: str  # day tooltip
    mnum: int  # month number
    ynum: int  # year number

    name: str = field(init=False)  # weekday
    rest: int = field(default=0, init=False)  # 1 if day is rest

    _wdays = ('Понедельник', 'Вторник', 'Среда', 'Четверг',
              'Пятница', 'Суббота', 'Воскресенье')
    _dtypes = ('Рабочий', 'Сокращенный', 'Выходной', 'Праздничный')

    def __post_init__(self):
        self.ttip = self._get_dtype()
        self.name = self._get_wday()
        self.rest = 1 if self.dtype in (2, 3) else 0

    def _get_wday(self):
        return self._wdays[self.dweek - 1]

    def _get_dtype(self):
        # Return ttip depends on day type
        if self.ttip == '':
            if self.dtype in range(0, len(self._dtypes)):
                return self._dtypes[self.dtype]
        else:
            return self.ttip

    def __str__(self):
        info = (f'{self.ynum}.{self.mnum:02d}.{self.dnum:02d}',
                f'| {self.dweek} {self.name:<11}',
                f'| {self.dtype} {self.ttip}')
        return ' '.join(info)


@dataclass
class ProcaMonth:
    '''Class to store month info'''

    ynum: int  # Year number
    mnum: int  # Month number
    rawdata: dict  # Days dict (keys = days numbers)

    # Calculated fields
    name: str = field(init=False)
    days: tuple = field(init=False)
    twork: int = field(init=False)
    trest: int = field(init=False)
    tdays: int = field(init=False)

    _mnames = ('Январь', 'Февраль', 'Март', 'Апрель',
               'Май', 'Июнь', 'Июль', 'Август',
               'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')

    def __post_init__(self):
        # Get month name
        self.name = self._get_mname()
        # Days namedtuple fields
        self.days = self._create_days()

        self.trest = sum(day.rest for day in self.days)
        self.tdays = len(self.days)
        self.twork = self.tdays - self.trest

    def _get_mname(self):
        return self._mnames[self.mnum - 1]

    def _create_day(self, dnum: str | int):
        # Day data as dictionary
        daydata = self.rawdata.get(str(dnum)) | {'mnum': self.mnum,
                                                 'ynum': self.ynum}
        return ProcaDay(**daydata)

    def _aliases(self):
        # Dict with renamed fields {original_key: renamed_key}
        return {dkey: 'd' + dkey for dkey in self.rawdata.keys()}

    def _create_days(self):
        # Make aliases for days ntuple (field names with prefix d1, d2..)
        aliases = self._aliases()
        # Declare Days ntuple
        Days = namedtuple('Days', aliases.values())
        # Collect days into namedtuple
        return Days(**{
            alias: self._create_day(dkey)
            for dkey, alias in aliases.items()
            })

    def __str__(self):
        return '\n'.join([day.__str__() for day in self.days])


class ProcaYear:
    '''Class to parse and store production calendar data'''

    def __init__(self, external_data: dict):
        self.ynum: int | None = None
        self.basic_data = external_data
        self._aliases = ('jan', 'feb', 'mar', 'apr', 'may', 'jun',
                         'jul', 'aug', 'sep', 'oct', 'nov', 'dec')

    @property
    def basic_data(self):
        return self._basic_data

    @basic_data.setter
    def basic_data(self, data):
        # Some input data checks
        if not isinstance(data, dict):
            raise ValueError('Input should be a dictionary') from None

        if len(data) == 0:
            raise ValueError('Passed dict has no keys') from None

        # Set year number, it depends on data input
        try:
            if len(str(ynum := int(tuple(data.keys())[0]))) == 4:
                self.ynum = ynum
        except ValueError:
            raise ValueError('Root key is not a 4-digit number') from None

        # Set data
        self._basic_data = data.get(str(self.ynum))

    def __call__(self, *mnums: int):
        # Validate arguments
        if len(mnums) == 0:
            # If no args passed make default list
            mnums = [n for n in range(1, 13)]
        elif len(mnums) > 12:
            raise ValueError('Number of args >12')

        if len([n for n in mnums if n not in range(1, 13)]) > 0:
            raise ValueError('Args values not in [1..12] range')

        if len(set(mnums)) != len(mnums):
            raise ValueError('Not unique args')

        self.months = self._months(*mnums)

        return self.months

    def _get_alias(self, mkey: str | int):
        if 1 <= (mnum := int(mkey)) <= len(self._aliases):
            return self._aliases[mnum - 1]
        else:
            return None

    def _create_month(self, mkey: str | int):
        # Create month: mkey = month number (1 = jan, 2 = feb...)
        return ProcaMonth(self.ynum, int(mkey), self.basic_data.get(str(mkey)))

    def _months(self, *mnums: int):
        # Collect months into a namedtuple with fields = aliases
        # mkey is str, mnums is a tuple | list of integers
        Months = namedtuple('Months', [self._get_alias(n) for n in mnums])
        return Months(**{
                self._get_alias(mkey): self._create_month(mkey)
                for mkey in self.basic_data.keys() if int(mkey) in mnums
                })


# if __name__ == '__main__':

#     import json

#     # Returns dictionary loaded from JSON file
#     def readJSON(fileName):
#         with open(fileName) as fileJSON:
#             data = json.load(fileJSON)
#         return data

#     # Create year object
#     year = ProcaYear(readJSON('sjob_2023_min.json'))

#     # Make 1st quarter months of the year
#     months = year(1, 2, 3, 4)
#     # Get January by alias 'jan'
#     jan = months.jan

#     # Print January days table
#     print(jan)
#     # Show January info using month fields
#     print(f'{jan.name}:',
#           f'рабочих дн: {jan.twork}',
#           f'выходных дн: {jan.trest}',
#           f'всего дн: {jan.tdays}',
#           sep='\n')

#     # Get 7th day of January
#     d7 = jan.days.d7
#     # Print day info table
#     print(d7)
#     # Show day info using day fields
#     print(f'дата: {d7.dnum:02d}.{d7.mnum:02d}.{d7.ynum}',
#           f'день недели: {d7.name}',
#           f'выходной день: {"Да" if d7.rest == 1 else "Нет"}',
#           f'праздник: {d7.ttip if d7.dtype == 3 else "Нет"}',
#           sep='\n')

#     # More examples:
#     # Make 12 months (it's default if not args passed)
#     months = year()

#     # Table header
#     stick = ' | '
#     fields_width = {'mnum': 2, 'name': 8, 'tdays': 4, 'twork': 4, 'trest': 4}
#     fields_ru = {'mnum': '#', 'name': 'мес.', 'tdays': 'дн.',
#                  'twork': 'раб.', 'trest': 'вых.'}

#     # Show table header
#     print(*[fields_ru[f].ljust(w) for f, w in fields_width.items()], sep=stick)

#     # Show top line
#     print('-' * (sum(fields_width.values()) + len(stick)*4))

#     # Show months info table
#     for m in months:
#         row = []
#         for f, w in fields_width.items():
#             if f == 'mnum':
#                 # 2 pos digit with leading zero
#                 cell = f'{getattr(m, f):02d}'.rjust(w)
#             else:
#                 cell = str(getattr(m, f)).ljust(w)
#             row.append(cell)
#         print(*row, sep=stick)

#     # Show bottom line
#     print('-' * (sum(fields_width.values()) + len(stick)*4))

#     # Calculate totals by 12 months
#     fields_total = ('tdays', 'twork', 'trest')
#     totals = {f: sum(getattr(m, f, 0) for m in months) for f in fields_total}
#     # Show table totals
#     print(*[str(totals[f]).ljust(w)
#             if f in fields_total
#             else ''.ljust(w)
#             for f, w in fields_width.items()], sep=' | ')
