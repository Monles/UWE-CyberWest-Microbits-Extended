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
        pass  # Constructor

    def random_int(self, _min, _max, sys_time):
        random.seed(sys_time)
        return random.randint(_min, _max)

    def data_string(self, new_group, delimiter):
        return "%s%s" % (new_group, delimiter)

def text_to_morse(text):
  # Define a dictionary mapping characters to Morse code
  morse_code_dict = {
      'A': '.-',
      'B': '-...',
      'C': '-.-.',
      'D': '-..',
      'E': '.',
      'F': '..-.',
      'G': '--.',
      'H': '....',
      'I': '..',
      'J': '.---',
      'K': '-.-',
      'L': '.-..',
      'M': '--',
      'N': '-.',
      'O': '---',
      'P': '.--.',
      'Q': '--.-',
      'R': '.-.',
      'S': '...',
      'T': '-',
      'U': '..-',
      'V': '...-',
      'W': '.--',
      'X': '-..-',
      'Y': '-.--',
      'Z': '--..',
      '0': '-----',
      '1': '.----',
      '2': '..---',
      '3': '...--',
      '4': '....-',
      '5': '.....',
      '6': '-....',
      '7': '--...',
      '8': '---..',
      '9': '----.',
      ' ': ' ',  # Space
      ',': '--..--',  # Mapping for comma
      '.': '.-.-.-',  # Mapping for period
      '?': '..--..',  # Mapping for question mark
      '/': '-..-.',  # Mapping for slash
      '(': '-.--.',  # Mapping for opening parenthesis
      ')': '-.--.-',  # Mapping for closing parenthesis
      '!': '− · − · − −',
  }

  # Convert text to uppercase to ensure all characters are handled consistently
  text = text.upper()

  # Convert each character in the text to Morse code and join them together
  morse_code = ' '.join([morse_code_dict.get(char, '') for char in text])

  return morse_code


def morse_to_text(morse_code):
  # Define a dictionary mapping Morse code to characters
  morse_code_dict = {
      '.-': 'A',
      '-...': 'B',
      '-.-.': 'C',
      '-..': 'D',
      '.': 'E',
      '..-.': 'F',
      '--.': 'G',
      '....': 'H',
      '..': 'I',
      '.---': 'J',
      '-.-': 'K',
      '.-..': 'L',
      '--': 'M',
      '-.': 'N',
      '---': 'O',
      '.--.': 'P',
      '--.-': 'Q',
      '.-.': 'R',
      '...': 'S',
      '-': 'T',
      '..-': 'U',
      '...-': 'V',
      '.--': 'W',
      '-..-': 'X',
      '-.--': 'Y',
      '--..': 'Z',
      '-----': '0',
      '.----': '1',
      '..---': '2',
      '...--': '3',
      '....-': '4',
      '.....': '5',
      '-....': '6',
      '--...': '7',
      '---..': '8',
      '----.': '9',
      '': ' ',  # Space (added to handle delimiter)
      '--..--': ',',
      '.-.-.-': '.',
      '..--..': '?',
      '-..-.': '/',
      '-.--.': '(',
      '-.--.-': ')',
      '− · − · − −': '!',
  }

  # Split Morse code into individual characters (letters) based on spaces
  morse_letters = morse_code.split(' ')

  # Convert each Morse code letter to its corresponding English character
  english_text = ''.join(
      [morse_code_dict.get(letter, '') for letter in morse_letters])

  return english_text

# Pairing instance
pairing = PairingClass()

# Handle all potential data incoming from the radio
def on_data_received():
    global pairing_started, paired, confirm_wait, confirmed, new_group

    # Now the micro-bit receives data of a pairing request 
    received_data = radio.receive()

    # If data is not empty
    if received_data is not None:

        # If the receiver micro-bit has already paired with The sender:
        # Then the receiver micro-bit will scroll the received data on the screen
        if paired:
            display.scroll(received_data)
        
        # HANDLE EMPTY DATA
        if received_data == "":
            pass  # Do nothing


        # HANDLE CONFIRMATION MESSAGE
        # (Explanation)
        elif confirm_wait and not paired:
            if received_data == CONFIRM_MESSAGE:
                paired = True
                confirm_wait = False

        # HANDLE POTENTIAL PAIRING DATA
        # (Explanation)
        elif not confirm_wait and not paired:

            # Get the running time of the board.
            started_waiting = running_time()

            while True:
                # Now the micro-bit is PAIRED! ➕
                display.show("+")
                
                # Wait for button input
                # Press Button A + Button B together to confirm the pairing request
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

    # messages = ["Hello", "Goodbye", "How are you?", "Shhh! Secret"]
    messages = [".... . .-.. .-.. ---", "--. --- --- -.. -... -.-- .", ".... --- .--   .- .-. .   -.-- --- ..- ", "... .... ....    ... . -.-. .-. . -"]
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
                    radio.send(selected_message)
                    message_sent = True
                
# Call the main function if the script is run directly
if __name__ == "__main__":
    main()