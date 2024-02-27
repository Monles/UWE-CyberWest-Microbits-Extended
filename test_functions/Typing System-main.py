# Imports go at the top
from microbit import *

def convert(s): 
    # initialization of string to "" 
    new = "" 
    # traverse in the string 
    for x in s: 
        new += x 
    # return string 
    return new 

s=[]
print('hi')
display.show(s) 


# Code in a 'while True:' loop repeats forever
while True:

    if button_a.is_pressed() and button_b.is_pressed():
        display.scroll('A and B')
        # finish
        print('finish')
        display.show(s)
        print(convert(s))
        
    elif button_a.is_pressed():
        display.scroll('A')
        s.append('.')
        print(s)
        
    elif button_b.is_pressed():
        display.scroll('B')
        s.append('-')
        print(s)
        display.show(s)
        
        
    elif pin_logo.is_touched():
        display.scroll('Logo')
        # add space to the string
        s.append(' ')
        print(s)
        display.show(s)
        
        
    # Shake the micro:bit to send messages
    elif accelerometer.was_gesture('shake'):
        # finish typing
        display.show(Image.ARROW_N)
        print("UP")
        print('Sending Message....')
        
    sleep(100)



