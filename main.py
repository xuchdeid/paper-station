import epaper2in13
from machine import Pin, SPI
import machine
import framebuf
from image_light import hello_world_light
from time import sleep_ms

button = Pin(39, Pin.IN)

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

#e.fb.text('Hello World', 30, 0, 1)

#e.fb.hline(30, 30, 10, 1)
#e.fb.vline(30, 50, 10, 1)
#e.fb.line(30, 70, 40, 80, 1)

fb = e.fb
run = True
count = 0
while run == True:
    if button.value() == 0:
        break;
    fb.fill(0)
    fb.rect(0, 0, 100, 100, 1)
    fb.text('CPU: %dMhz' % (machine.freq()/1000/1000), 2, 5, 1)
    fb.text('count: %d' % (count), 2, 15, 1)
    e.update()
    count+=1
    sleep_ms(1000)
print("Good bye!")