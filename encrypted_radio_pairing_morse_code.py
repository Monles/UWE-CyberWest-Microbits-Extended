# Import necessary libraries
from microbit import *
import radio
import random

# Global variables
pairing_started = False
paired = False
confirm_wait = False
confirmed = False
new_group = 0
encryption_key = 0b10101010

# Constants
CONFIRM_MESSAGE = "confirm"
PAIR_DELIMITER = ","

# Class to handle pairing
class PairingClass:
    def __init__(self):
        pass  # Constructor

    def random_int(self, _min, _max, sys_time):
        random.seed(sys_time)
        return random.randint(_min, _max)

    def data_string(self, new_group, delimiter):
        return f"{new_group}{delimiter}"


# ------------------------------------------------------------------
# You need to turn the radio on before you use it.
# Because the radio feature uses more power,
# You might want to turn it off at certain times to save batteries:
# ------------------------------------------------------------------

# Initialize radio
radio.on()

# Initialize pairing
pairing = PairingClass()


# ------------------------------------------------------------------
# Some functions 
#   - Waht are they used to do?
#   - Check it out to find some vulnerabilities... 💀
#   - Is there any function wrong?
# ------------------------------------------------------------------

# Function to encrypt a message
def encrypt(message):
    return "".join(chr(ord(char) ^ encryption_key) for char in message)

# Function to decrypt a message
def decrypt(encrypted_message):
    return encrypt(encrypted_message)  # Decryption is the same as encryption

# Handle all potential data incoming from the radio
def on_data_received():
    received_data = radio.receive()
    if received_data is not None:
        if paired:
            display.scroll(decrypt(received_data))
        # Handle pairing process...
        # Handle other scenarios...
        
        # HANDLE EMPTY DATA
        if received_data == "":
            pass  # Do nothing

        # HANDLE CONFIRMATION MESSAGE
        elif confirm_wait and not paired:
            if received_data == CONFIRM_MESSAGE:
                paired = True
                confirm_wait = False

        # HANDLE POTENTIAL PAIRING DATA
        elif not confirm_wait and not paired:
            started_waiting = running_time()
            while True:
                display.show("+")
                
                # Wait for button input
                if button_a.is_pressed() and button_b.is_pressed():
                    display.clear()
                    data_list = received_data.split(PAIR_DELIMITER)
                    new_group = int(data_list[0])
                    confirmed = True
                    pairing_started = False
                    display.scroll(int(data_list[0]))
                    break

                # Don't pair if the user doesn't confirm within 10 seconds
                elif running_time() - started_waiting > 10000:
                    display.show("X")
                    sleep(700)
                    display.clear()
                    pairing_started = False
                    break
    

# Function to initiate pairing
def initiate_pairing():
    global pairing_started
    # Handle pairing process...
    # Wait for button input to initiate pairing...
    # Handle user confirm...
    # Handle start pairing...
    # Handle complete pairing...

# Main function
def main():
    
    # Set flags
    paired = False
    pairing_started = False
    confirm_wait = False
    confirmed = False

    # Handle pairing procedure
    while True:
        on_data_received()

        # Wait for button input to initiate pairing
        if button_b.is_pressed():
            pairing_started = True
            print("B pressed")

        # Handle user confirm
        on_data_received()
        sleep(100)
        if confirmed:
            radio.send(CONFIRM_MESSAGE)
            paired = True
            pairing_started = False

        # Handle start pairing
        elif pairing_started:
            display.scroll("PAIRING")
            new_group = pairing.random_int(0, 255, running_time())
            sleep(100)
            random_nums = pairing.data_string(new_group, PAIR_DELIMITER)
            radio.send(random_nums)
            sleep(100)
            started_waiting = running_time()
            confirm_wait = True
            while True:
                on_data_received()
                sleep(50)
                if paired:
                    display.scroll(new_group)
                    confirm_wait = False
                    pairing_started = False
                    break
                elif running_time() - started_waiting > 10000:
                    display.scroll("X")
                    pairing_started = False
                    confirm_wait = False
                    break

        # Handle complete pairing
        if paired:
            radio.config(group=new_group)
            paired = True
            pairing_started = False
            confirm_wait = False
            confirmed = False
            break

    # Clears buffer
    radio.send("")

    messages = ["Hello", "Goodbye", "How are you?", "Shhh! it's secret"]
    current_message_index = 0
   

    # Main loop
    while True:
        on_data_received()

        message_sent = False

        if button_a.is_pressed() and paired:
            display.scroll(messages[current_message_index], wait=False)
            sleep(500)  # Adjust as needed

            while not message_sent:
                if button_a.is_pressed():
                    current_message_index = (current_message_index + 1) % len(messages)
                    display.scroll(messages[current_message_index], wait=False)
                    sleep(500)  # Adjust as needed
    
                if button_b.is_pressed():
                    display.clear()
                    selected_message = messages[current_message_index]
                    encrypted_message = encrypt(selected_message)
                    radio.send(encrypted_message)
                    message_sent = True
                
# Call the main function if the script is run directly
if __name__ == "__main__":
    main()