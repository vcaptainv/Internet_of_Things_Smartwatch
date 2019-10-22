import network
import socket
import ssd1306
import machine
from machine import Pin
import json
import time
import urequests

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
spi = machine.SPI(1, baudrate=2000000, polarity=1, phase=1)
cs = machine.Pin(15, machine.Pin.OUT)

button_press = 0
json_list = []
Amazon_server= "http://18.218.34.7/post"

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        display_text("Connecting...")
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    display_text(str(sta_if.ifconfig()[0]))
    return sta_if.ifconfig()

# Display String
def display_text(str):
    oled.fill(0)
    oled.text(str, 0, 0)
    oled.show()

def press_button(p):
    global button_press
    # debounce
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)

    if button_press == 0:
        button_press = 1
        display_text("Start")
    else:
        button_press = 0
        display_text("Stop")

def data_collection():
    global button_press, json_list
    #Read a number of bytes specified by nbytes while continuously writing
    #the single byte given by write. Returns a bytes object with the data that was read.
    cs.value(0)
    x = spi.read(5, 0xf3) # register 33: X-Axis Data 1 # read 5 bytes
    cs.value(1)

    cs.value(0)
    y = spi.read(5, 0xf5) # register 35: Y-Axis Data 1 # read 5 bytes
    cs.value(1)
    display_text(str(x[1])+","+str(y[1]))
    json_data = {"x":x[1],"y":y[1]}
    json_list.append(json_data)
    time.sleep(0.1)

def start_accel():
    power_ctl = b'\x2d\x2b'
    cs.value(0)
    spi.write(power_ctl)
    cs.value(1)
    #0x31 --> data format control
    data_format = b'\x31\x34'
    cs.value(0)
    spi.write(data_format)
    cs.value(1)

def main():
    start_accel()
    button_B = Pin(2, Pin.IN, Pin.PULL_UP)
    button_B.irq(trigger=Pin.IRQ_FALLING, handler=press_button)

    ip_addr = do_connect()
    while True:
        if button_press:
            for i in range(20):
                data_collection()
            break
    display_text("Finish collecting...")
    count = 0
    for i in range (len(json_list)):
        display_text(str(count))
        json_data = json.dumps(json_list[i])
        reply = urequests.post(url = Amazon_server, data = json_data)
        count += 1
        time.sleep(0.1)
    display_text("Finish sending...")

if __name__ == '__main__':
    main()
