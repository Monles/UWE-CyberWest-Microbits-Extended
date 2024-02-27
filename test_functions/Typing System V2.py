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

message = []

# Main loop
while True:

    message_sent = False

    if button_a.is_pressed():
        # display.scroll(messages[current_message_index], wait=False)
        display.scroll("START...")
        sleep(500)  # Adjust as needed

        while not message_sent:
            if button_a.is_pressed():
                display.scroll('A')
                message.append('.')
                print(message)
                sleep(500)  # Adjust as needed

            if button_b.is_pressed():
                display.scroll('B')
                message.append('-')
                print(message)
                display.show(message)
                sleep(500)  # Adjust as needed

            if pin_logo.is_touched():
                display.scroll('L')
                # add space to the string
                message.append(' ')
                print(message)
                display.show(message)

            if button_a.is_pressed() and button_b.is_pressed():
                display.scroll('A and B')
                # finish
                print('finish')
                display.show(message)
                print(convert(message))
                sleep(500)  # Adjust as needed

            # Shake the micro:bit to send messages
            if accelerometer.was_gesture('shake'):
                # finish typing
                display.show(Image.ARROW_N)
                print("UP")
                print('Sending Message....')
                display.clear()
                selected_message = convert(message)
                sleep(500)  # Adjust as needed

            sleep(100)
                        


