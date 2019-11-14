import gdeh0213b72b
from gdeh0213b72b import GxEPD_BLACK, GxEPD_WHITE
from machine import Pin, SPI, Timer
import machine
from res.icon import demo
from time import sleep_ms
import uasyncio as asyncio
import esp32

button_state = 0


def initEPaper():
    cs = Pin(5)
    dc = Pin(17)
    rst = Pin(16)
    busy = Pin(4)

    sck = Pin(18)
    miso = Pin(19)
    mosi = Pin(23)
    spi = SPI(2, baudrate=20000000, polarity=0,
              phase=0, sck=sck, miso=miso, mosi=mosi)

    device = gdeh0213b72b.EPD(spi, cs, dc, rst, busy)
    return device


def initButton():
    button = Pin(39, Pin.IN)
    return button


async def mainUI():
    global button_state
    device = initEPaper()
    count = 10
    canvas = device.fb
    while True:
        canvas.fill(0)
        #canvas.rect(0, 0, 100, 100, 1)
        #canvas.text('CPU: %dMhz' % (machine.freq()/1000/1000), 2, 5, 1)
        #canvas.text('count: %d' % (count), 2, 15, 1)
        #canvas.text('button: %d' % button_state, 2, 25, 1)
        #canvas.text('temp: %d' % esp32.raw_temperature(), 2, 35, 1)
        y = 0
        icon = demo
        device.drawBitmap(icon['bytes'], 0, 0, icon['meta']
                          ['width'], icon['meta']['height'])
        await device.update()
        count += 1
        await asyncio.sleep_ms(50000)


async def buttonEvent(loop):
    button = initButton()
    while True:
        check(loop, button)
        await asyncio.sleep_ms(100)


def check(loop, button):
    global button_state
    button_state = button.value()
    if button_state == 0:
        loop.stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(buttonEvent(loop))
    loop.create_task(mainUI())
    loop.run_forever()
    loop.close()
    print("Good bye!")
