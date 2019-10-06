from time import sleep
from machine import Pin

def main():
    led1 = Pin(0, Pin.OUT)
    led2 = Pin(2, Pin.OUT)


    #intial states
    led1.value(1)
    led2.value(1)
    count = 0

    while True:
        if count < 4 :
            led1.value(0)
            sleep(0.5)
            led1.value(1)
            sleep(0.5)
            count += 1
        else:
            led2.value(0)
            led1.value(0)
            sleep(0.5)
            led2.value(1)
            led1.value(1)
            sleep(0.5)
            count = 0

main()
