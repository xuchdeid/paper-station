import uasyncio as asyncio
from calendar import Calendar
from todo import Todo
from space import Space
from machine import Pin
from ui.display import getDisplay
import utime

button_state = 0
loop = None


def initButton():
    button = Pin(39, Pin.IN)
    return button


async def mainUI():
    display = getDisplay()
    views = []
    views.append(Calendar())
    y = views[0].width
    views.append(Space(y, 0, 5, display.height))
    y += views[1].width
    views.append(Todo(y, 0))

    while True:
        for view in views:
            view.draw()
        await display.update()
        await asyncio.sleep_ms(diff60Seconds())


def diff60Seconds():
    data = utime.localtime()
    second = data[5]
    return (60 - second) * 1000


async def buttonEvent():
    button = initButton()
    while True:
        await check(button)
        await asyncio.sleep_ms(100)


async def check(button):
    global button_state, loop

    button_state = button.value()
    if button_state == 0:
        loop.stop()
    else:
        return 0


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(buttonEvent())
    loop.create_task(mainUI())
    loop.run_forever()
    loop.close()
    print("Good bye!")
