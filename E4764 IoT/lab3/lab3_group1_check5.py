import machine
import ssd1306
import time

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
#initialize spi
spi = machine.SPI(1, baudrate=2000000, polarity=1, phase=1)
#initialize chip select
#CS is the serial port enable line and is controlled by the SPI master.
#This line must go low at the start of a transmission and high at the end of a transmission
cs = machine.Pin(15, machine.Pin.OUT)

def coord():
    #Read a number of bytes specified by nbytes while continuously writing
    #the single byte given by write. Returns a bytes object with the data that was read.    
    cs.value(0)
    x = spi.read(5, 0xf3) # register 33: X-Axis Data 1 # read 5 bytes
    cs.value(1)

    cs.value(0)
    y = spi.read(5, 0xf5) # register 35: Y-Axis Data 1 # read 5 bytes
    cs.value(1)

    return x[1], y[1] #


def main():
    #0x2d --> power control
    power_ctl = b'\x2d\x2b'
    cs.value(0)
    spi.write(power_ctl)
    cs.value(1)
    
    #0x31 --> data format control
    data_format = b'\x31\x34'
    cs.value(0)
    spi.write(data_format)
    cs.value(1)
    
    #initialize (x,y) coordinatess
    px = 0
    py = 0
    while True:
        x, y = coord()
        
        if 0 < x < 128:
            px -= x
        elif x > 128:
            px += (256 - x)
        

        if 0 < y < 128:
            py += y
        elif y > 128:
            py -= (256 - y)

        if px >= 128:
            px = 0
        if px < 0:
            px = 128
        if py >= 32:
            py = 0
        if py < 0:
            py = 32
            
        oled.fill(0)
        oled.text("IoT is Fun!", px, py)
        oled.show()
        time.sleep(0.01)


if __name__ == '__main__':

    main()
