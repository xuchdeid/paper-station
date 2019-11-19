from ui.canvas import Canvas
import utime
import machine


class Calendar(Canvas):

    def __init__(self, startX=0, startY=0):
        Canvas.__init__(self, startX, startY, 122, 122)
        self.textCalendar = [
            '', 'Su Mo Tu We Th Fr Sa', '', '', '', '', '', '']
        self.fillArea = [-1, -1, -1]
        self.lastYearAndMonth = [-1, -1]
        self.up = False

    def onDraw(self):
        self.toCalendar()
        color = True
        y = 3
        for i in range(0, 7):
            if i == 0:
                dh = 10
            else:
                dh = 12
            self.drawText(self.textCalendar[i], 1, y, color)
            if self.fillArea[1] != -1 and i == self.fillArea[1]:
                size = self.fillArea[0] * 3
                self.fill(size*6 - 1, y - 3, size*6 + dh, y+9, color)
                self.drawText('%2d' %
                              self.fillArea[2], size*6 + 1, y, not color)
            self.drawLine(0, y + dh, self.width - 1, y + dh, color)
            y += 18

    def onEvent(self, event):
        pass

    def isLeapYear(self, year):
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    def daysOfMonth(self, year, month):
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif month in (4, 6, 9, 11):
            return 30
        elif month == 2:
            if self.isLeapYear(year):
                return 29
            else:
                return 28
        else:
            return -1

    def toCalendar(self):
        data = utime.localtime()
        year = data[0]
        month = data[1]
        day = data[2]
        hour = data[3]
        minute = data[4]
        second = data[5]
        weekday = (data[6] + 1) % 7
        step = (8 - (day - weekday) % 7) % 7

        machine.RTC().init((year, month, day + 1, 4, hour, minute, 0, 0))

        self.fillArea[0] = weekday
        self.fillArea[2] = day

        self.textCalendar[0] = '%02d/%02d   %02d:%02d   %4d' % (
            month, day, hour, minute, year)

        if self.lastYearAndMonth[0] == year and self.lastYearAndMonth[1] == month:
            for _i in range(0, 6):
                index = _i + 2
                for _j in range(0, 7):
                    _n = _i * 7 + _j - step + 1
                    if _n == day:
                        self.fillArea[1] = index
                        if self.fillArea[1] >= 7:
                            self.fillArea[1] -= 1
                            if not self.up:
                                self.up = True
                                for index in range(0, 5):
                                    self.textCalendar[2 +
                                                      index] = self.textCalendar[3 + index]
                        return
        else:
            self.lastYearAndMonth[0] = year
            self.lastYearAndMonth[1] = month
            self.up = False

        max_day = self.daysOfMonth(year, month)
        for _i in range(0, 6):
            index = _i + 2
            self.textCalendar[index] = ''
            _day = None
            for _j in range(0, 7):
                if _i == 0 and _j < step:
                    self.textCalendar[index] += '   '
                else:
                    _n = _i * 7 + _j - step + 1
                    if _n == day:
                        self.fillArea[1] = index
                    if _n > max_day:
                        self.textCalendar[index] += '  '
                        if _j != 6:
                            self.textCalendar[index] += ' '
                        break
                    else:
                        _temp = (_n,)
                        if _day == None:
                            _day = _temp
                        else:
                            _day = _day + _temp
                        self.textCalendar[index] += '%2d'
                        if _j != 6:
                            self.textCalendar[index] += ' '
            if _day != None:
                self.textCalendar[index] = self.textCalendar[index] % _day

        if self.fillArea[1] >= 7:
            self.fillArea[1] -= 1
            if not self.up:
                self.up = True
                for index in range(0, 5):
                    self.textCalendar[2 + index] = self.textCalendar[3 + index]
