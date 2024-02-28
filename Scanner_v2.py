# Only receive group ID

from microbit import *
import radio

# Radio configuration
radio.on()

# Constants
PAIR_DELIMITER = ","

# Gloobal variables
new_group = 0
sn = False
paired = False

# Function to handle receiving messages
def receive_messages():
    global sn, paired
    received_data = radio.receive()
    while True:
        if sn == False:
            if received_data is not None:
                print("Not sniffing")
                data_list = received_data.split(PAIR_DELIMITER)
                new_group = int(data_list[0])
                radio.config(group=new_group)
                sn=True
                display.scroll(new_group)
                print(new_group)
                break
        if sn == True:
            if received_data is not None:
                print("sniffing")
                print(received_data)
                display.scroll(received_data)
                break
        if received_data == "":
            pass
            

# Main function
def main():
    while True:
        print("scanning...")
       
        # Start receiving messages
        receive_messages()
        sleep(100)
        receive_messages()
        sleep(100)
        

# Call the main function if the script is run directly
if __name__ == "__main__":
    main()