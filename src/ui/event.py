BUTTON_EVENT = const(Event('button'))


class Event:

    def __init__(self, name):
        self.name = name
        self.value = -1
