from machine import Pin
from time import sleep

def main():
    led = Pin(2, Pin.OUT)

    for i in range(3):
        led.value(0)
        sleep(0.5)
        led.value(1)
        sleep(0.5)
    for i in range(3):
        led.value(0)
        sleep(1.5)
        led.value(1)
        sleep(0.5)
    for i in range(3):
        led.value(0)
        sleep(0.5)
        led.value(0.5)
        sleep(0.5)




        
if __name__ == '__main__':
     main()
