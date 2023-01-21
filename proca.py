#! python3
#
# proca module is for working with production calendar in JSON files
# JSON files should be prepared with procaparser

class ProcaYear:

    def __init__(self, fData) -> None:
        # Get the first year key
        for strYear in fData.keys():
            self.year = fData[strYear]
            try:
                year = strYear
            except ValueError:
                return None
            # Skip the rest keys
            break

        self.year_num = year

    def _checkMonth(self, monthNum):
        if type(monthNum) in (int, str) and str(monthNum) in self.year.keys():
            return str(monthNum)

    def getMonth(self, monthNum):
        if monthNum := self._checkMonth(monthNum):
            return self.ProcaMonth(monthNum, self.year[monthNum])

    # Returns data according to path 'month_num.day_num'
    def select(self, path, sep='.'):
        monthNum, dayNum = None, None

        # Check path like 1.31 (month.day)
        path = str(path).partition(sep)
        if ''.join(path[1:]) == '':
            # If path consists on only one number
            monthNum = int(path[0])
        elif path[1] == sep:
            # If path is breakable by sep
            monthNum, dayNum = int(path[0]), int(path[2])

        # Return data
        if monthNum and not dayNum:
            # month  only
            return self.getMonth(monthNum)
        elif monthNum and dayNum:
            # month_num.day_num
            return self.getMonth(monthNum).getDay(dayNum)

    # Print year months
    def printMe(self):
        for ind in range(1, 13):
            self.ProcaMonth(str(ind), self.year[str(ind)]).printMe()

    class ProcaMonth:

        def __init__(self, monthNum, monthData) -> None:
            self.mon_num = monthNum  # month number
            self.mon_name = monthData['name']  # month name
            self.days_total = monthData['countdays']  # total days in month
            self.days_rest = monthData['restdays']  # the rest days count
            self.days_work = monthData['workdays']  # workdays counter
            self.days = monthData['days']  # per day description

        def _checkDay(self, dayNum):
            if type(dayNum) in (int, str) and str(dayNum) in self.days:
                return str(dayNum)

        def getDay(self, dayNum):
            if dayNum := self._checkDay(dayNum):
                return self.days[dayNum]

        def isWork(self, dayNum):
            if dayNum := self._checkDay(dayNum):
                return self.days[dayNum]['dtype_num'] == 0

        def isRest(self, dayNum):
            if dayNum := self._checkDay(dayNum):
                return self.days[dayNum]['dtype_num'] in (1, 3)

        # Month formatted output as table
        def printMe(self, header={}, gap='.', hide=False):
            # Check args
            if len(header) == 0:
                # 'column_name': column_width
                header = {
                    'day_num': 10,
                    'wday_num': 10,
                    'wday_str': 14,
                    'dtype_num': 10,
                    'dtype_str': 50
                    }
            if len(gap) == 0:
                gap = '.'

            # Show month name
            print(self.mon_name.ljust(sum(header.values()), ' '))

            # Show header line
            if not hide:
                print(*[key.ljust(header[key], ' ') for key in header], sep='')

            # Iterate over days in asc order
            for ind in range(1, len(self.days) + 1):
                day = self.days[str(ind)]
                # Show values in according to header
                print(*[str(day[key]).ljust(header[key], gap) for key in header], sep='')
