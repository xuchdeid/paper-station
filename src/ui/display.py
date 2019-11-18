import ui.gdeh0213b72b
from ui.gdeh0213b72b import EPD, GxEPD_BLACK, GxEPD_WHITE
from machine import Pin, SPI

device = None


def getDisplay():
    global device
    if device == None:
        cs = Pin(5)
        dc = Pin(17)
        rst = Pin(16)
        busy = Pin(4)

        sck = Pin(18)
        miso = Pin(19)
        mosi = Pin(23)
        spi = SPI(2, baudrate=20000000, polarity=0,
                  phase=0, sck=sck, miso=miso, mosi=mosi)

        device = EPD(spi, cs, dc, rst, busy)
    return device
