from display import getDisplay
from font import render


class Canvas:
    def __init__(self):
        self.device = getDisplay()

    def drawPixel(self, x, y, color):
        self.device.drawPixel(x, y, color)

    def drawBitmap(self, bitmap, x, y, width, height):
        self.device.drawBitmap(bitmap, x, y, width, height)

    def drawText(self, str, x, y, color):
        for i in range(0, 10):
            buffer = render(i)
            _x = x + 8 * i
            self.drawBitmap(buffer, _x, y, 1, 8)

    def onDraw(self):
        pass

    def fill(self, color):
        self.device.fillScreen(color)

    async def draw(self):
        self.onDraw()
        await self.device.update()
