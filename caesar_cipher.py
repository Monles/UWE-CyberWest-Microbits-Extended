from microbit import * 
import radio 
import random 

# Constants 
CONFIRM_MESSAGE = "confirm" 
PAIR_DELIMITER = "," 

# Global variables 
pairing_started = False 
paired = False 
confirm_wait = False 
confirmed = False 
new_group = 0 

# Radio configuration 
radio.on() 

# Pairing class 
class PairingClass: 
    def __init__(self): 
        pass  
    
# Random number generator for the radio group number
def random_int(self, _min, _max, sys_time): 
    random.seed(sys_time) 
    return random.randint(_min, _max) 

def data_string(self, new_group, delimiter): 
    return "%s%s" % (new_group, delimiter) 

  

# Pairing instance 
pairing = PairingClass() 


# Function to encrypt a message with a Caesar cipher shift of -7 (adjust the shift as needed)
def encrypt(message):  

    encrypted_message = ""  

    for char in message:  
        # The ord() function returns the Unicode code point value of each letter in our plaintext.
        if char.isupper():   
            # The modulo operation ensures the shifted Unicode value is within the value range of A-Z.
            shifted_char = chr(((ord(char) - ord('A') - 7) % 26) + ord('A'))  
            encrypted_message += shifted_char  

        elif char.islower():  
            # This modulo operation ensures the shifted Unicode value is within the value range of a-z.
            shifted_char = chr(((ord(char) - ord('a') - 7) % 26) + ord('a'))  
            encrypted_message += shifted_char  

        else: 
            encrypted_message += char  

    return encrypted_message  


# Function to decrypt a message (not called, adjust the code to do so if needed according to the aim of your lesson) 
def decrypt(encrypted_message): 

    decrypted_message = "" 

    for char in encrypted_message:          
        if char.isupper():   
            # Make sure this matches the shift value. Our encryption function is a shift of -7.
            # So, we need to shift the ciphertext by +7 to decrypt. Knowing this, can you retrieve the full key?
            shifted_char = chr(((ord(char) - ord('A') + 7) % 26) + ord('A'))  
            decrypted_message += shifted_char  

        elif char.islower():  
            shifted_char = chr(((ord(char) - ord('a') + 7) % 26) + ord('a'))  
            decrypted_message += shifted_char  

        else: 
            decrypted_message += char  

    return decrypted_message 

  

# Handle all potential data incoming from the radio 

def on_data_received(): 

    global pairing_started, paired, confirm_wait, confirmed, new_group 

    received_data = radio.receive() 

    if received_data is not None: 
        if paired: 
            display.scroll(received_data)  

    
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

     

# Main function 
def main(): 
    global pairing_started, paired, confirm_wait, confirmed, new_group 

    # Set flags 
    paired = False 
    pairing_started = False 
    confirm_wait = False 
    confirmed = False 

    # Handle pairing procedure 
    while True: 
        on_data_received() 

        # Press button B on one microbit to initiate pairing 
        if button_b.is_pressed(): 
            pairing_started = True 
            print("B pressed") 

        # Handle user confirm (To confirm pairing, press buttons A+B on the other microbit device once the + button is shown)
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

    # Here is a Python list containing a choice of messages in plaintext. You may change these as you wish.
    # The microbit will scroll these on its display. 
    # Press button A to scroll to the next message and B to choose one to be encrypted and sent.
    messages = ["This is a Caesar cipher", "It is easy to break", "Try frequency analysis", "Are Caesar ciphers really secure?"] 
    current_message_index = 0 


    # Main loop 
    while True: 
        on_data_received() 

        message_sent = False 

        if button_a.is_pressed() and paired: 
            display.scroll(messages[current_message_index], wait=False) 
            sleep(500)  # The sleep() function pauses code execution for n milliseconds. Adjust as needed 

            while not message_sent: 
                # Scroll through messages with button A if you are not already sending one
                if button_a.is_pressed(): 
                    current_message_index = (current_message_index + 1) % len(messages) 
                    display.scroll(messages[current_message_index], wait=False) 
                    sleep(500) 

                if button_b.is_pressed(): 
                    # Encrypt and send the message of your choice
                    display.clear() 
                    selected_message = messages[current_message_index] 
                    encrypted_message = encrypt(selected_message) 
                    radio.send(encrypted_message) 
                    message_sent = True 

# Call the main function if the script is run directly 
if __name__ == "__main__": 

    main() 