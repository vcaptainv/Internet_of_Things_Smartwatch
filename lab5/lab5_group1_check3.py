import network
import socket
import ssd1306
import machine

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
rtc = machine.RTC()
rtc.datetime((2019, 10, 13, 5, 0, 0, 0, 0))
screen_on = True
time_on = False

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

# Update Command onto Screen
def display_screen(str):
    global screen_on, time_on
    if screen_on == True:
        if time_on == True:
            display_time()
        else:
            display_text(str)
    else:
        oled.fill(0)
        oled.show()

# Query Current Time
def display_time():
    datetime = rtc.datetime()
    oled.fill(0)
    date_str = str(rtc.datetime()[0])+"/"+str(rtc.datetime()[1])+"/"+str(rtc.datetime()[2])
    time_str = str(rtc.datetime()[4])+":"+str(rtc.datetime()[5])+":"+str(rtc.datetime()[6])
    oled.text(date_str, 0, 0)
    oled.text(time_str, 0, 10)
    oled.show()


def main():
    global screen_on, time_on
    ip_addr = do_connect()
    addr = socket.getaddrinfo(ip_addr[0], 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(addr)
    s.listen(1)

    while True:
        client_socket, client_addr = s.accept()

        request = client_socket.recv(2048)
        request = str(request)

        if 'msg' in request:
            # Decode and Parse the response HTTP string
            msg = request.split('/?msg=')[1].split('HTTP')[0]
            msg = msg.replace('%20', ' ')

            if 'screen on' in msg:
                screen_on = True
            if 'screen off' in msg:
                screen_on = False

            if 'time on' in msg:
                time_on = True
            if 'time off' in msg:
                time_on = False

            display_screen(msg)
            
        # Send Response back to Android App
        response = "HTTP/1.1 200 OK\r\n\r\n" + msg
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    main()
