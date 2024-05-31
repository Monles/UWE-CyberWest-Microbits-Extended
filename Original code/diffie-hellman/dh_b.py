# Code for microbit B 

from microbit import * 
import radio 
import random 

# Constants 
p = 23 # 'large' prime number
g = 5 # integer coprime to p, ie GCD(g,p)={1}

radio_group = 10 # Change number for each pair of participants. Must be integer between 0 and 83 inclusive

# Function to calculate (g^b) % p 

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

received_key_a_flag = False 

# Wait for public key A from microbit A 
while not received_key_a_flag: 
    received_data = radio.receive() 
    if received_data is not None: 
        received_key_a = int(received_data) # Potential for MitM here?
        display.scroll("R") 
        display.scroll(received_key_a) 
        received_key_a_flag = True 

# Generate private key b 
private_key_b = random.randint(1, p - 1) 

# Calculate public key b
public_key_b = mod_exp(g, private_key_b, p) 
radio.send(str(public_key_b)) 
display.scroll("PKB sent") 

# Calculate shared secret 
shared_secret = mod_exp(received_key_a, private_key_b, p) 

# Display shared secret 
display.scroll(str(shared_secret), wait=False, loop=True) 

sleep(5000) 

# Derive encryption key from shared secret to encrypt messages