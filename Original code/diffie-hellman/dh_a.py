# Code for microbit A 

from microbit import * 
import radio  
import random

# Constants 
p = 23 # 'large' prime number
g = 5 # integer coprime to p, ie GCD(g,p)={1}
radio_group = 10 # Change number for each pair of participants. Must be integer between 0 and 83 inclusive


# Function to calculate (g^a) % p 
def mod_exp(base, exponent, modulus): 
    result = 1 
    while exponent > 0: 
        if exponent % 2 == 1: 
            result = (result * base) % modulus 
        exponent = exponent // 2 
        base = (base * base) % modulus 
    return result 

# Configure radio 
radio.on() 
radio.config(group=radio_group) 

received_key_b_flag = False

# Wait for button press to start the key exchange 
while not button_a.is_pressed(): 
    pass 

# Generate private key a 
private_key_a = random.randint(1, p - 1) 

# Calculate public key A 
public_key_a = mod_exp(g, private_key_a, p) 

# Send public key A over radio
if button_a.is_pressed():
    radio.send(str(public_key_a)) 
    display.scroll("PKA sent")

# Wait for public key B from microbit B 
received_data = radio.receive() 
if received_data is not None: 
    received_key_b = int(received_data) # Potential for MitM here?
    display.scroll("R")
    display.scroll(received_key_b)
    received_key_b_flag = True

# Calculate shared secret 
if received_key_b_flag:
    shared_secret = mod_exp(received_key_b, private_key_a, p) 
    display.scroll(str(shared_secret), wait=False, loop=True) 
    sleep(5000) 

# Derive encryption key from shared secret to encrypt messages