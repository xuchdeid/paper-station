from ui.canvas import Canvas
#from res.icon import demo

titles = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

gap = const(1)

fontWidth = const(8)

fontHeight = const(8)

width = const((fontWidth*2 + gap)*7 + gap)


class Calendar(Canvas):

    def __init__(self, startX=0, startY=0):
        self.width = 122
        self.height = 122
        Canvas.__init__(self, startX, startY, self.width, self.height)

    def onDraw(self):
        #icon = demo
        # self.drawBitmap(icon['bytes'], 0, 0, icon['meta']
        #                ['width'], icon['meta']['height'])
        color = True
        y = 3
        dh = 12
        self.drawText('11/18   16:27   2019', 1, y, color)
        self.drawLine(0, y + 10, self.width - 1, y + 10, color)
        y += 18
        self.drawText('Su Mo Tu We Th Fr Sa', 1, y, color)
        self.drawLine(0, y + dh, self.width - 1, y + dh, color)
        y += 18
        self.drawText('       1  2  3  4  5', 1, y, color)
        self.drawLine(0, y + dh, self.width - 1, y + dh, color)
        y += 18
        self.drawText(' 6  7  8  9 10 11 12', 1, y, color)
        self.drawLine(0, y + dh, self.width - 1, y + dh, color)
        y += 18
        self.drawText('13 14 15 16 17 18 19', 1, y, color)
        self.fill(15*6 - 1, y - 3, 15*6 + 12, y+9, color)
        self.drawText('18', 15*6, y, not color)
        self.drawLine(0, y + dh, self.width - 1, y + dh, color)
        y += 18
        self.drawText('20 21 22 23 24 25 26', 1, y, color)
        self.drawLine(0, y + dh, self.width - 1, y + dh, color)
        y += 18
        self.drawText('27 28 29 30          ', 1, y, color)

    def onEvent(self, event):
        pass
