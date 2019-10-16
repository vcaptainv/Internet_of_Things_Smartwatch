import network
import machine
import ssd1306
import urequests
import json
import time

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        # oled.fill(0)
        # oled.text('connecting to network...', 0, 0)
        # oled.show()
        sta_if.active(True)
        sta_if.connect(b'Columbia University')
        while not sta_if.isconnected():
            pass
    str_builder = str(sta_if.ifconfig())
    oled.fill(0)
    oled.text(str_builder, 0, 0)
    oled.show()
#
# def get_location():
#     data = {
#          "considerIp": "true"
#     }
#     json_data = json.dumps(data)
#     reply = urequests.post(url = API_ENDPOINT+API_KEY, data = json_data)
#     reply_dict = reply.json()
#     lat = reply_dict["location"]["lat"]
#     lng = reply_dict["location"]["lng"]
#
#     return lat, lng
#
# def get_weather(x,y):
#     #sample API url & key
#     weather_api_key =
#     weather_call ="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}".format(x,y)
#
#     reply = urequests.get(url =weather_call+weather_api_key )
#     reply_dict = reply.json()
#     temp = reply_dict["main"]["temp"]
#     description = reply_dict["weather"][0]["description"]
#
#     return temp, description

def send_twitter():
    tweet = {"value2" : "#ThinkHarder!", "value1": "to debug Micropython"}

    twt_url =
    twitter = urequests.post(url = twt_url, json = tweet) # pure genius library


def main():
    do_connect()
    # while True:
        # x, y = get_location()

    #    temp, description = get_weather(x,y)
    send_twitter()

    oled.fill(1)
    # oled.text( str(temp-273), 0, 0)
    # oled.text( str(description) , 0,10)

    oled.show()
    # time.sleep()


if __name__ == '__main__':
    main()
