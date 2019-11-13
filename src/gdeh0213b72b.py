"""
MicroPython 2.13" Black/White GDEH0213B72B e-paper display driver

MIT License
Copyright (c) 2019 xuchdeid

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from micropython import const
import framebuf
import uasyncio as asyncio

# Display resolution
EPD_WIDTH = const(128)
EPD_HEIGHT = const(250)
EPD_VISIBLE_WIDTH = const(122)
EPD_VISIBLE_HEIGHT = const(250)
# datasheet says 250x122 (increased to 128 to be multiples of 8)

# Display commands
DRIVER_OUTPUT_CONTROL = const(0x01)
Gate_Driving_Voltage_Control = const(0x03)
Source_Driving_voltage_Control = const(0x04)
BOOSTER_SOFT_START_CONTROL = const(0x0C)  # not in datasheet
# GATE_SCAN_START_POSITION             = const(0x0F) # not in datasheet
DEEP_SLEEP_MODE = const(0x10)
DATA_ENTRY_MODE_SETTING = const(0x11)
SW_RESET = const(0x12)
ANALOG_BLOCK_CONTROL = const(0x74)
DIGITAL_BLOCK_CONTROL = const(0x7E)
#TEMPERATURE_SENSOR_CONTROL           = const(0x1A)
MASTER_ACTIVATION = const(0x20)
#DISPLAY_UPDATE_CONTROL_1             = const(0x21)
DISPLAY_UPDATE_CONTROL_2 = const(0x22)
# Panel Break Detection           \x23
WRITE_RAM = const(0x24)
WRITE_VCOM_REGISTER = const(0x2C)
# Status Bit Read                 \x2F
WRITE_LUT_REGISTER = const(0x32)
SET_DUMMY_LINE_PERIOD = const(0x3A)
SET_GATE_TIME = const(0x3B)
BORDER_WAVEFORM_CONTROL = const(0x3C)
SET_RAM_X_ADDRESS_START_END_POSITION = const(0x44)
SET_RAM_Y_ADDRESS_START_END_POSITION = const(0x45)
SET_RAM_X_ADDRESS_COUNTER = const(0x4E)
SET_RAM_Y_ADDRESS_COUNTER = const(0x4F)
TERMINATE_FRAME_READ_WRITE = const(0xFF)  # not in datasheet, aka NOOP

BUSY = const(1)  # 1=busy, 0=idle
GxGDE0213B72B_PU_DELAY = const(300)
GxEPD_BLACK = const(0)
GxEPD_WHITE = const(1)


class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self._buffer = bytearray(EPD_WIDTH * EPD_HEIGHT // 8)
        self.fb = framebuf.FrameBuffer(
            self._buffer, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)
        self.fillScreen(GxEPD_WHITE)

    LUT_FULL_UPDATE = bytearray(
        b'\xA0\x90\x50\x00\x00\x00\x00\x00\x00\x00' +
        b'\x50\x90\xA0\x00\x00\x00\x00\x00\x00\x00' +
        b'\xA0\x90\x50\x00\x00\x00\x00\x00\x00\x00' +
        b'\x50\x90\xA0\x00\x00\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
        b'\x0F\x0F\x00\x00\x00' +
        b'\x0F\x0F\x00\x00\x03' +
        b'\x0F\x0F\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x17\x41\xA8\x32\x50\x0A\x09')

    LUT_PARTIAL_UPDATE = bytearray(
        b'\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
        b'\x80\x00\xA0\x00\x00\x00\x00\x00\x00\x00' +
        b'\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
        b'\x80\x00\xA0\x00\x00\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
        b'\x0A\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x00\x00\x00\x00\x00' +
        b'\x15\x41\xA8\x32\x50\x2C\x0B')

    GDOControl = [0x01, (EPD_HEIGHT - 1) % 256, (EPD_HEIGHT - 1) % 256, 0x00]
    softstart = [0x0c, 0xd7, 0xd6, 0x9d]
    VCOMVol = [0x2c, 0xa8]
    DummyLine = [0x3a, 0x1a]
    Gatetime = [0x3b, 0x08]

    async def update(self):
        await self.init_full()
        await self._command(0x24)
        w = EPD_WIDTH//8
        self.fb.scroll(0, 1)
        for y in range(0, EPD_HEIGHT):
            for x in range(0, w):
                idx = (EPD_HEIGHT - y) * w + x
                if idx < len(self._buffer):
                    self._data(bytearray([~self._buffer[idx]]))
                else:
                    self._data(bytearray([~0x00]))
        await self.update_full()
        await self._powerOff()

    def clear(self):
        self.fillScreen(GxEPD_WHITE)

    def fillScreen(self, color):
        if color == GxEPD_BLACK:
            for i in range(0, len(self._buffer)):
                self._buffer[i] = 0xFF
        else:
            for i in range(0, len(self._buffer)):
                self._buffer[i] = 0x00

    async def _command(self, command, data=None):
        if self.busy.value() == BUSY:
            str = 'command 0x%X' % command
            await wait_until_idle(str)

        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    async def init(self):
        await self.reset()
        await self.wait_until_idle('_InitDisplay')
        await self._command(SW_RESET)
        await self.wait_until_idle('_InitDisplay')
        await self._command(ANALOG_BLOCK_CONTROL)
        self._data(bytearray([0x54]))
        await self._command(DIGITAL_BLOCK_CONTROL)
        self._data(bytearray([0x3B]))

        await self._command(DRIVER_OUTPUT_CONTROL)
        self._data(bytearray([0xF9]))
        self._data(bytearray([0x00]))
        self._data(bytearray([0x00]))

        await self._command(DATA_ENTRY_MODE_SETTING)
        self._data(bytearray([0x01]))

        await self._command(SET_RAM_X_ADDRESS_START_END_POSITION)
        self._data(bytearray([0x00]))
        self._data(bytearray([0x0F]))

        await self._command(SET_RAM_Y_ADDRESS_START_END_POSITION)
        self._data(bytearray([0xF9]))
        self._data(bytearray([0x00]))
        self._data(bytearray([0x00]))
        self._data(bytearray([0x00]))

        await self._command(BORDER_WAVEFORM_CONTROL)
        self._data(bytearray([0x03]))

        await self._command(WRITE_VCOM_REGISTER)
        self._data(bytearray([0x50]))

        await self._command(Gate_Driving_Voltage_Control)
        self._data(bytearray([self.LUT_FULL_UPDATE[100]]))

        await self._command(Source_Driving_voltage_Control)
        self._data(bytearray([self.LUT_FULL_UPDATE[101]]))
        self._data(bytearray([self.LUT_FULL_UPDATE[102]]))
        self._data(bytearray([self.LUT_FULL_UPDATE[103]]))

        await self._command(SET_DUMMY_LINE_PERIOD)
        self._data(bytearray([self.LUT_FULL_UPDATE[105]]))
        await self._command(SET_GATE_TIME)
        self._data(bytearray([self.LUT_FULL_UPDATE[106]]))

        await self._command(WRITE_LUT_REGISTER)
        for i in range(0, 100):
            self._data(bytearray([self.LUT_FULL_UPDATE[i]]))
        await self._command(SET_RAM_X_ADDRESS_COUNTER)
        self._data(bytearray([0x00]))
        await self._command(SET_RAM_Y_ADDRESS_COUNTER)
        self._data(bytearray([0xF9]))
        self._data(bytearray([0x00]))
        await self.wait_until_idle('_InitDisplay')

    async def wait_until_idle(self, info=None):
        while self.busy.value() == BUSY:
            await asyncio.sleep_ms(100)

    async def _powerOn(self):
        await self._command(DISPLAY_UPDATE_CONTROL_2)
        self._data(bytearray([0xC0]))
        await self._command(MASTER_ACTIVATION)
        await self.wait_until_idle('_PowerOn')

    async def _powerOff(self):
        await self._command(DISPLAY_UPDATE_CONTROL_2)
        self._data(bytearray([0xC3]))
        await self._command(MASTER_ACTIVATION)
        await self.wait_until_idle('_PowerOff')

    async def init_full(self):
        await self.init()
        await self._command(WRITE_LUT_REGISTER, self.LUT_FULL_UPDATE)
        await self._powerOn()

    async def init_part(self):
        await self.init()
        await self._command(WRITE_LUT_REGISTER, self.LUT_PARTIAL_UPDATE)
        await self._powerOn()

    async def update_full(self):
        await self._command(DISPLAY_UPDATE_CONTROL_2)
        self._data(bytearray([0xC7]))
        await self._command(MASTER_ACTIVATION)
        await self.wait_until_idle('_Update_Full')

    async def update_part(self):
        await self._command(DISPLAY_UPDATE_CONTROL_2)
        self._data(bytearray([0x04]))
        await self._command(MASTER_ACTIVATION)
        await self.wait_until_idle('_Update_Part')
        await self._command(TERMINATE_FRAME_READ_WRITE)

    async def reset(self):
        self.rst(0)
        await asyncio.sleep_ms(100)
        self.rst(1)
        await asyncio.sleep_ms(100)

    def drawBitmap(self, bitmap, width, height, startX, startY):
        max_w = EPD_WIDTH//8
        for h in range(startY, height + startY):
            for w in range(0, width):
                if w < max_w and h < EPD_HEIGHT:
                    value = bitmap[(h - startY) * width + w]
                    idx = h * max_w + w
                    old = self._buffer[idx]
                    self._buffer[idx] = value | old
