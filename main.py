import epaper2in13
from machine import Pin, SPI
import framebuf
from image_light import hello_world_light

cs = Pin(5)
dc = Pin(17)
rst = Pin(16)
busy = Pin(4)

sck = Pin(18)
miso = Pin(19)
mosi = Pin(23)
spi = SPI(2, baudrate=20000000, polarity=0,
          phase=0, sck=sck, miso=miso, mosi=mosi)

e = epaper2in13.EPD(spi, cs, dc, rst, busy)
e.init()

e.clear_frame_memory(0xff)

print('hello world')
