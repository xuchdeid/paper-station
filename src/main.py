import uasyncio as asyncio
from calendar import Calendar
from todo import Todo
from machine import Pin
from ui.display import getDisplay

button_state = 0
loop = None


def initButton():
    button = Pin(39, Pin.IN)
    return button


async def mainUI():
    display = getDisplay()
    calendar = Calendar()
    todo = Todo(calendar.width + 5, 0)
    #calendar.startX = display.width - calendar.width

    while True:
        calendar.draw()
        todo.draw()
        await display.update()
        await asyncio.sleep_ms(60000)


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
