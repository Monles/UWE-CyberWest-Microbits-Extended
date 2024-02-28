# Only receive group ID

from microbit import *
import radio

# Radio configuration
radio.on()

# Constants
PAIR_DELIMITER = ","

# Gloobal variables
new_group = 0
sniffing = False

# Function to handle receiving messages
def receive_messages():
    global new_group
    while True:
        received_data = radio.receive()
       
        if received_data is not None:
            if new_group == 0:
                data_list = received_data.split(PAIR_DELIMITER)
                new_group = int(data_list[0])
                radio.config(group=new_group)
            display.scroll(received_data)
            print(received_data)
            
            

# Main function
def main():
    while True:
        # Start receiving messages
        receive_messages()
    
    # Create an empty array for storing characters of the message
    message = []

    # Main loop
    while True:
        on_data_received()

# Call the main function if the script is run directly
if __name__ == "__main__":
    main()