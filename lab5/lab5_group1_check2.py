import network
import socket
import ssd1306
import machine

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        display_text("Connecting...")
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    display_text("Connnected!")
    
    return sta_if.ifconfig()

def display_text(str):
    oled.fill(0)
    oled.text(str, 0, 0)
    oled.show()

def main():
    ip_addr = do_connect()
    addr = socket.getaddrinfo(ip_addr[0], 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(1)

    while True:
        client_socket, client_addr = s.accept()

        request = client_socket.recv(2048)
        request = str(request)
        # Send Response back to Android App
        response = "HTTP/1.1 200 OK\r\n\r\n"
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    main()
