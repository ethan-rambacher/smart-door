import RPi.GPIO as gp

gp.setmode(gp.BOARD)
gp.setup(40, gp.OUT)#sets pin 40 as an output
gp.output(40, gp.HIGH) #sets pin 40 to high or low




def turn_led_on():
    print("Turning the led on!")
    



def turn_led_off():
    print("Turning the led off!")
    

