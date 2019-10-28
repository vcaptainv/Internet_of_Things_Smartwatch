import network
import socket as soc
from socket import socket, AF_INET, SOCK_STREAM
import ssd1306
import machine
from machine import I2C, RTC, Pin, ADC, PWM
import time
import gc
import urequests
import json

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
spi = machine.SPI(1, baudrate=2000000, polarity=1, phase=1)
cs = machine.Pin(15, machine.Pin.OUT)
button_press = 0
Amazon_server= "18.218.34.7"
str_builder = ""
adc = machine.ADC(0)
rtc = machine.RTC()
rtc.datetime((2019, 10, 27, 0, 0, 0, 0, 0))
dict_index = 0
rtc_datetime = {"year":0, "month":1, "day":2, "hour":4, "minute":5, "second":6}
alarm = 0
alarm_time = {"hour":0, "minute":0, "second":25}
API_KEY = "AIzaSyAuVBCra8qfLX5TSHYI8hb_1n5rDY2V4oA" #Jason's key
API_ENDPOINT = "https://www.googleapis.com/geolocation/v1/geolocate?key="
screen_on = True
time_on = False
weather = False
Twitter = False
gesture_on = False

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

def display_text(str):
    oled.fill(0)
    oled.text(str, 0, 0)
    oled.show()
    
def memfree():
    gc.collect()
    gc.mem_free()
    
def get_location():
    data = {
         "considerIp": "true"
    }
    json_data = json.dumps(data)
    reply = urequests.post(url = API_ENDPOINT+API_KEY, data = json_data)
    reply_dict = reply.json()
    lat = reply_dict["location"]["lat"]
    lng = reply_dict["location"]["lng"]
    return lat, lng

def get_weather(x,y):
    weather_api_key = "&appid=34ff8085d3b99815d850093dda28e624"
    weather_call ="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}".format(x,y)
    reply = urequests.get(url = weather_call + weather_api_key )
    reply_dict = reply.json()
    temp = reply_dict["main"]["temp"]
    description = reply_dict["weather"][0]["description"]
    return temp, description
    
def display_date_time(button_B):
    global button_press
    button_press = 0
    button_B.irq(trigger=Pin.IRQ_FALLING, handler=press_button_B)
    while True:
        if button_press == 0:
            oled.contrast(adc.read())
            global alarm
            oled.fill(0)
            str_builder_date = "Date:"
            str_builder_date += str(rtc.datetime()[rtc_datetime["year"]]) + '/' + str(rtc.datetime()[rtc_datetime["month"]]) + '/' + str(rtc.datetime()[rtc_datetime["day"]])
            str_builder_time = "Time:"
            str_builder_time += str(rtc.datetime()[rtc_datetime["hour"]]) + ':' + str(rtc.datetime()[rtc_datetime["minute"]]) + ':' + str(rtc.datetime()[rtc_datetime["second"]])
            str_builder_alarm_time = "Alarm:" + str(alarm_time["hour"]) + ':' + str(alarm_time["minute"]) + ':' + str(alarm_time["second"])
            oled.text(str_builder_date, 0, 0)
            oled.text(str_builder_time, 0, 10)
            oled.text(str_builder_alarm_time, 0, 20)
            oled.show()
            if alarm ==1 and (rtc.datetime()[4] == alarm_time["hour"] and rtc.datetime()[5] == alarm_time["minute"]):
                display_alarm()
        else:
            button_B.irq(trigger=Pin.IRQ_FALLING, handler=increment_by_one)
            break
            
def display_alarm():
    led = PWM(Pin(13),freq=1000,duty=812)
    display_text("Alarm!!")
    time.sleep(1)
    
def debounce(p):
    active = 0
    while active < 20:
        if p.value() == 0:
            active += 1
        else:
            return
        time.sleep_ms(1)
    
def change_alarm_setting(p):
    global alarm
    debounce(p)
    alarm += 1
    alarm = alarm % 2
    alarm_mode= ['Alarm: off', 'Alarm: on']
    display_text(alarm_mode[alarm])

def increment_by_one(p):
    global dict_index, rtc_datetime, rtc, alarm
    debounce(p)
    date_time_keys = list(rtc_datetime.keys())
    alarm_time_keys = list(alarm_time.keys())
    if alarm == 0:
        cur_datetime = list(rtc.datetime())
        cur_datetime[rtc_datetime[date_time_keys[dict_index]]] += 1
        rtc.datetime(tuple(cur_datetime))
    elif alarm == 1:
        alarm_time[alarm_time_keys[dict_index]] += 1

def data_collection():
    global str_builder
    memfree()
    cs.value(0)
    x = spi.read(5, 0xf3)
    cs.value(1)
    cs.value(0)
    y = spi.read(5, 0xf5)
    cs.value(1)
    display_text(str(x[1])+","+str(y[1]))
    str_builder += (str(x[1])+","+str(y[1])+",")
    time.sleep(0.15)

def start_accel():
    power_ctl = b'\x2d\x2b'
    cs.value(0)
    spi.write(power_ctl)
    cs.value(1)
    data_format = b'\x31\x34'
    cs.value(0)
    spi.write(data_format)
    cs.value(1)
    
def press_button_B(p):
    global button_press
    debounce(p)
    if button_press == 0:
        button_press = 1
    else:
        button_press = 0
        
def gesture(button_B):
    global button_press, str_builder, gesture_on
    button_B.irq(trigger=Pin.IRQ_FALLING, handler=press_button_B)
    start_accel()
    display_text("Sample")
    while True:
        if button_press:
            for i in range(20):
                data_collection()
            break
    serverName = Amazon_server
    serverPort = 8080
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(str_builder.encode('utf-8'))
    response = clientSocket.recv(1024)
    display_text(str(response.decode('utf-8')))
    button_press = 0
    display_text("Predict {}".format(response))
    str_builder = ""
    button_B.irq(trigger=Pin.IRQ_FALLING, handler=increment_by_one)
    gesture_on = False
    clientSocket.close()

def display_weather():
    x, y = get_location()
    temp, description = get_weather(x,y)
    oled.fill(0)
    oled.text( str(temp-273), 0, 0)
    oled.text( str(description) , 0,10)
    oled.show()

def send_twitter(msg):
    global Twitter
    tweet = {"value2" : "{}".format(msg) , "value1" : " "}
    twt_url = "https://maker.ifttt.com/trigger/tweet/with/key/cHsQR-Qfw8rX88SVIpLOOH"
    twitter = urequests.post(url = twt_url, json = tweet) # pure genius library
    display_text("twitter: {}".format(msg))
    Twitter = False    

def display_screen(button_B, msg):
    global screen_on,time_on,weather,Twitter
    if screen_on == True:
        if time_on == True:
            display_date_time(button_B)
        elif weather == True:
            display_weather()  
        elif gesture_on == True:
            gesture(button_B)
        else:
            display_text(msg)
        if Twitter == True:
            send_twitter(msg)  
    else:
        oled.fill(0)
        oled.show()

def speech_to_text(button_B, s):
    global screen_on,time_on,weather,Twitter,gesture_on
    display_text("Listening...")
    while True:
        memfree()
        client_socket, client_addr = s.accept()
        request = str(client_socket.recv(2048))
        if 'msg' in request:
            msg = request.split('/?msg=')[1].split('HTTP')[0]
            msg = msg.replace('%20', ' ')
            if 'screen on' in msg:
                screen_on = True
            if 'screen off' in msg:
                screen_on = False
            if 'time on' in msg:
                time_on = True
                weather = False
            if 'time off' in msg:
                time_on = False
            if 'weather on' in msg:
                weather = True
                time_on = False
            if 'weather off' in msg:
                weather = False
                time_on = True
            if 'send Twitter' in msg:
                Twitter = True
            if 'gesture' in msg:
                gesture_on = True
                weather = False
                time_on = False
            display_screen(button_B, msg)
        response = "HTTP/1.1 200 OK\n\n" + msg
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

def main():
    global alarm
    memfree()
    button_A = Pin(12, Pin.IN, Pin.PULL_UP)
    button_B = Pin(2, Pin.IN, Pin.PULL_UP)
    button_C = Pin(14, Pin.IN, Pin.PULL_UP)
    button_C.irq(trigger=Pin.IRQ_FALLING, handler=change_alarm_setting)
    ip_addr = do_connect()
    addr = soc.getaddrinfo(ip_addr[0], 80)[0][-1]
    s = soc.socket(AF_INET, SOCK_STREAM)
    s.bind(addr)
    s.listen(1)
    speech_to_text(button_B,s)
        
if __name__ == '__main__':
    main()
