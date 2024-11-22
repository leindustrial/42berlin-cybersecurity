#!/usr/bin/env python3

import os
import base64

key_hex = os.urandom(32).hex() #64-character hex key
#key_base32 = base64.b32encode(bytes.fromhex(key_hex)).decode('utf-8') # -> to base 32

print(f"Generated Hex Key: {key_hex}")
#print(f"Generated Base32 Key: {key_base32}")

# Write the key to a file
with open("key.hex", "w") as file:
    file.write(key_hex)

print("Saved to file -> key.hex")