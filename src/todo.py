from ui.canvas import Canvas


class Todo(Canvas):

    def __init__(self, startX=0, startY=0, width=-1, height=-1):
        Canvas.__init__(self, startX, startY, width, height)
        self.width = 250 - startX + 1
        self.height = 122

    def onDraw(self):
        y = 3
        lineHeight = 14
        self.drawText('Today:', 0, y, 1)
        y += lineHeight
        self.drawText('=>', 0, y, 1)
        y += lineHeight
        self.drawText('  Boss out of office', 0, y, 1)
        y += lineHeight
        self.drawText('12:00-13:00:', 0, y, 1)
        y += lineHeight
        self.drawText('  Important Meeting', 0, y, 1)
        y += lineHeight
        self.drawText('16:00-17:00:', 0, y, 1)
        y += lineHeight
        self.drawText('  boring Meeting', 0, y, 1)
