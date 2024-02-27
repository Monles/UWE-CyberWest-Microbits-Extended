from microbit import *
import radio

# Constants
PAIR_DELIMITER = ","

# Gloobal variables
new_group = 0
sni = False

# Radio configuration
radio.on()

# Function to handle receiving messages
def receive_messages():
    while True:
        received_data = radio.receive()
        
        if received_data is not None:
            if sni is False:
                data_list = received_data.split(PAIR_DELIMITER)
                new_group = int(data_list[0])
                radio.config(group=new_group)
                display.scroll(int(received_data))
                print(int(received_data)) 
                sniff = True
                break
        
        if (received_data is not None) and (sni == True):
            display.scroll(received_data)
            
         # HANDLE EMPTY DATA
        if received_data == "":
            pass  # Do nothing


# Main function
def main():
    while True:
        # Start receiving messages
        receive_messages()
        if sni == True:
            break
    


    # Main loop
    while True:
        receive_messages()


# Call the main function if the script is run directly
if __name__ == "__main__":
    main()