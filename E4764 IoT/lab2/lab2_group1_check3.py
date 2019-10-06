import time	
import machine
from machine import Pin,PWM

#checkpoint 3

#this variable keeps track of the state of the button
motion = False

#Debounce a button press.
#If the button is pressed fast enough (i.e. < 20ms),
#the button will hold onto its previous state.
def debounce(pin):
	temp = pin.value()
	state=0
	while state<20:
		if pin.value() == temp:
			state+=1
		else:
			state=0
		time.sleep_ms(1)  
        
#an interrupt is generated once when the button is pushed 
#and once when the button is let go  
def interrupt_handler(p):
    global motion
    if motion == False:
        debounce(p)
        motion = True
    else:
        debounce(p)
        motion = False

def main():
    global motion
    adc=machine.ADC(0)
    input1 = Pin(14, Pin.IN)
    input1.irq(trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), handler=interrupt_handler)
    
    #The system is activated when the button is pressed and deactivated when released. 
    #While activated, the LED and piezo changes brightness and pitch depending on the light sensor readings.
    
    while(True):
        time.sleep_ms(200)
        if motion==False:
            pwm13.deinit() #for LED
            pwm15.deinit() #for Piezo
        else:
            pwm13 = PWM(Pin(13) , freq=1000, duty=adc.read())
            pwm15 = PWM(Pin(15) , freq=adc.read(), duty=512)
        
    
if __name__ == '__main__':
     main()