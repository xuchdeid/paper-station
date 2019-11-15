from ui.canvas import Canvas
from res.icon import demo


class Calendar(Canvas):

    def onDraw(self):
        #icon = demo
        # self.drawBitmap(icon['bytes'], 0, 0, icon['meta']
        #                ['width'], icon['meta']['height'])
        self.drawText('', 0, 0, 1)

    def onEvent(self, event):
        pass
