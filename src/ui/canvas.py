from ui.display import getDisplay
from ui.font import render


class Canvas:
    def __init__(self, startX=0, startY=0, width=-1, height=-1):
        self.device = getDisplay()
        self._startX = startX
        self._startY = startY
        self._width = width
        self._height = height

    @property
    def startX(self):
        return self._startX

    @startX.setter
    def startX(self, val):
        self._startX = val

    @property
    def startY(self):
        return self._startY

    @startY.setter
    def startY(self, val):
        self._startY = val

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val

    def drawPixel(self, x, y, color):
        self.device.drawPixel(x + self._startX, y + self._startY, color)

    def drawBitmap(self, bitmap, x, y, width, height):
        self.device.drawBitmap(bitmap, x + self._startX,
                               y + self._startY, width, height)

    def drawText(self, string, x, y, color):
        self.device.fb.text(string, x + self._startX,
                            y + self._startY + 6, color)

    def drawLine(self, x0, y0, x1, y1, color):
        self.device.fb.line(x0 + self._startX, y0 + self._startY + 6,
                            x1 + self._startX, y1 + self._startY + 6, color)

    def onDraw(self):
        pass

    def clean(self):
        self.fill(0, 0, self.width - 1, self.height - 1, 0)

    def fill(self, x0, y0, x1, y1, color):
        if x0 > x1 or y0 > y1:
            return
        if x0 < 0:
            x0 = 0
        elif x0 >= self.width:
            x0 = self.width - 1
        if y0 < 0:
            y0 = 0
        elif y0 >= self.height:
            y0 = self.height - 1
        if x1 < 0:
            x1 = 0
        elif x1 >= self.width:
            x1 = self.width - 1
        if y1 < 0:
            y1 = 0
        elif y1 >= self.height:
            y1 = self.height - 1

        for i in range(y0, y1 + 1):
            for j in range(x0, x1 + 1):
                self.drawPixel(j, i, color)

    def draw(self):
        self.clean()
        self.onDraw()
