import machine
from machine import I2C, RTC, Pin, ADC, PWM
import ssd1306
import time

i2c = I2C(-1, machine.Pin(5), machine.Pin(4))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
adc = machine.ADC(0)

rtc = machine.RTC()
rtc.datetime((2019, 9, 25, 0, 0, 1, 0, 0))

dict_index = 0
rtc_datetime = {"year":0, "month":1, "day":2, "hour":4, "minute":5, "second":6}

alarm = 0
alarm_time = {"hour":0, "minute":0, "second":0}

def select_change_option(p):
    global dict_index, rtc_datetime, alarm_time
    dict_index += 1
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)
    
    if alarm == 0:
        dict_index = dict_index % 6
        display.fill(0) #clear the screen first  
        date_time_keys = list(rtc_datetime.keys())
        display.text('change: '+ str(date_time_keys[dict_index]), 0, 10)
        display.show()
    else:
        dict_index = dict_index % 3
        display.fill(0)
        alarm_time_keys = list(alarm_time.keys())
        display.text('change: '+ str(alarm_time_keys[dict_index]), 0, 10)
        display.show()
    

def change_alarm_setting(p):
    global alarm
    # debounce
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)

    alarm += 1
    alarm = alarm % 2
    alarm_mode= ['Alarm: off', 'Alarm: on']
    display.fill(0)
    display.text(alarm_mode[alarm], 0, 0)
    display.show() 


def increment_by_one(p):
    global dict_index, rtc_datetime, rtc, alarm
    # debounce
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)
    
    date_time_keys = list(rtc_datetime.keys())
    alarm_time_keys = list(alarm_time.keys())
    if alarm == 0:
        cur_datetime = list(rtc.datetime())
        cur_datetime[rtc_datetime[date_time_keys[dict_index]]] += 1
        rtc.datetime(tuple(cur_datetime))
    elif alarm == 1:
        
        alarm_time[alarm_time_keys[dict_index]] += 1
    
def display_date_time():
    global alarm
    display.fill(0)

    str_builder_date = "Date:"
    str_builder_date += str(rtc.datetime()[rtc_datetime["year"]]) + '/' + str(rtc.datetime()[rtc_datetime["month"]]) + '/' + str(rtc.datetime()[rtc_datetime["day"]])
    
    str_builder_time = "Time:"
    str_builder_time += str(rtc.datetime()[rtc_datetime["hour"]]) + ':' + str(rtc.datetime()[rtc_datetime["minute"]]) + ':' + str(rtc.datetime()[rtc_datetime["second"]])
    
    str_builder_alarm_time = "Alarm:" + str(alarm_time["hour"]) + ':' + str(alarm_time["minute"]) + ':' + str(alarm_time["second"])
    
    display.text(str_builder_date, 0, 0)
    display.text(str_builder_time, 0, 10)
    display.text(str_builder_alarm_time, 0, 20)
    display.show()


def display_alarm():
    led = PWM(Pin(13),freq=1000,duty=812)
    display.fill(0)
    display.text("Alarm", 0, 10)
    display.show()
    time.sleep(1)
    led.deinit()
    #deactivate alarm
    alarm = 0
        
        
def main():
    button_A = Pin(12, Pin.IN, Pin.PULL_UP)
    button_B = Pin(2, Pin.IN, Pin.PULL_UP)
    button_C = Pin(14, Pin.IN, Pin.PULL_UP)

    button_A.irq(trigger=Pin.IRQ_FALLING, handler=select_change_option)
    button_B.irq(trigger=Pin.IRQ_FALLING, handler=increment_by_one)
    button_C.irq(trigger=Pin.IRQ_FALLING, handler=change_alarm_setting)
    
    while True:
        display.contrast(adc.read())
        display_date_time()
        
        #must be in alarm mode to sound an alarm
        if alarm ==1 and (rtc.datetime()[4] == alarm_time["hour"] and rtc.datetime()[5] == alarm_time["minute"]):
            display_alarm()
        
        time.sleep(1)
    
    
if __name__ == '__main__':
    main()