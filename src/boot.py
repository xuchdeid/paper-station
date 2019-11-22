# This is script that run when device boot up or wake from sleep.
import network
import ntptime

ssid = 'WeWork'
password = 'P@ssw0rd'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

ntptime.settime()
