import time	
import machine
from machine import Pin,PWM

#checkpoint 2

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
    #Pin.IRQ_FALLING: to trigger the interrupt whenever the pin goes from HIGH to LOW;
    #Pin.IRQ_RISING: to trigger the interrupt whenever the pin goes from LOW to HIGH.
    #Initialize pin 14 for the reading of input from the button
    input1 = Pin(14, Pin.IN)
    input1.irq(trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), handler=interrupt_handler)
        
    
if __name__ == '__main__':
     main()