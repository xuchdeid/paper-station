# This is script that run when device boot up or wake from sleep.
import machine

machine.RTC().init((2019, 11, 19, 4, 17, 32, 0, 0))
