import requests
import json
import time

API_KEY = "AIzaSyAuVBCra8qfLX5TSHYI8hb_1n5rDY2V4oA" #Jason's key
API_ENDPOINT = "https://www.googleapis.com/geolocation/v1/geolocate?key="


def get_location():
    data = {
         "considerIp": "true"
    }
    json_data = json.dumps(data)
    reply = requests.post(url = API_ENDPOINT+API_KEY, data = json_data)
    reply_dict = reply.json()
    lat = reply_dict["location"]["lat"]
    lng = reply_dict["location"]["lng"]

    return lat, lng
def get_weather(x,y):
    weather_api_key = "&appid=34ff8085d3b99815d850093dda28e624"
    weather_call ="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}".format(x,y)
    reply = requests.get(url =weather_call+weather_api_key )
    reply_dict = reply.json()
    temp = reply_dict["main"]["temp"]
    description = reply_dict["weather"][0]["description"]

    return temp, description

def send_twitter():
    tweet = {
        "value1" : "#Thinkagain!"
    }

    twt_url= "https://maker.ifttt.com/trigger/tweet/with/key/cHsQR-Qfw8rX88SVIpLOOH"
    twitter = requests.post(url = twt_url, data = tweet)


def main():
    # x, y = get_location()
    #
    # temp, description = get_weather(x,y)

    # print(str(temp-273.0), description)

    send_twitter()
    print("hi")
if __name__ == '__main__':
    main()
