from machine import Pin, PWM,ADC
import time

#Function that changes the brightness of an LED and the pitch of a piezo in
#accordance to readings from the light sensor. 
def main():
    #initialize the ADC pin
    adc=machine.ADC(0)
    #The more light that reaches the sensor, the brighter 
    #the LED shines (the higher the duty cycle) 
    #and the higher the pitch from the piezo will be (the higher the frequency).
    while(True):
        pwm13 = PWM(Pin(13) , freq=5000, duty=adc.read())
        pwm15 = PWM(Pin(15) , freq=adc.read(), duty=512)

    
if __name__ == "__main__":
    main()