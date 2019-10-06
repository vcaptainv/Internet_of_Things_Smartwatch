import machine
from machine import I2C, RTC, Pin, ADC
import ssd1306
import time


i2c = I2C(-1, machine.Pin(5), machine.Pin(4))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
adc = machine.ADC(0)

rtc = machine.RTC()
rtc.datetime((2019, 9, 25, 0, 3, 0, 0, 0))
rtc_datetime = {"year":0, "month":1, "day":2, "hour":4, "minute":5, "second":6}
dict_index = 0

# change which pos do you want to change
def select_change_option(p):
    global dict_index, rtc_datetime
    dict_index += 1
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)
        
    display.fill(0) #clear the screen first
    dict_index = dict_index % 6
    date_time_keys = list(rtc_datetime.keys())
    display.text(str(date_time_keys[dict_index]), 10, 10)
    display.show()

def increment_by_one(p):
    global dict_index, rtc_datetime, rtc
    # debounce
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)

    cur_datetime = list(rtc.datetime())
    date_time_keys = list(rtc_datetime.keys())
    cur_datetime[rtc_datetime[date_time_keys[dict_index]]] += 1
    rtc.datetime(tuple(cur_datetime))


    
def display_date_time():
    display.fill(0)

    str_builder_date = "Date:"
    str_builder_date += str(rtc.datetime()[rtc_datetime["year"]]) + '/' + str(rtc.datetime()[rtc_datetime["month"]]) + '/' + str(rtc.datetime()[rtc_datetime["day"]])
    
    str_builder_time = "Time:"
    str_builder_time += str(rtc.datetime()[rtc_datetime["hour"]]) + ':' + str(rtc.datetime()[rtc_datetime["minute"]]) + ':' + str(rtc.datetime()[rtc_datetime["second"]])

    display.text(str_builder_date, 0, 0)
    display.text(str_builder_time, 0, 10)
    display.show()
    
def main():
    button_A = Pin(12, Pin.IN, Pin.PULL_UP)
    button_B = Pin(2, Pin.IN, Pin.PULL_UP)

    button_A.irq(trigger=Pin.IRQ_FALLING, handler=select_change_option)
    button_B.irq(trigger=Pin.IRQ_FALLING, handler=increment_by_one)
    
    while True:
        display.contrast(adc.read())
        display_date_time()
        time.sleep(1)
    
    
if __name__ == '__main__':
    main()