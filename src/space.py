from ui.canvas import Canvas


class Space(Canvas):

    def __init__(self, startX=0, startY=0, width=-1, height=-1):
        Canvas.__init__(self, startX, startY, width, height)
