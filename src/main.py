import uasyncio as asyncio
from calendar import Calendar
from machine import Pin

button_state = 0
loop = None


def initButton():
    button = Pin(39, Pin.IN)
    return button


async def mainUI():
    calendar = Calendar()
    while True:
        calendar.fill(0)
        await calendar.draw()
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
