#!/usr/bin/env python3

import os
# import base64

key_hex = os.urandom(32).hex() #64-character hex key

print(f"Generated Hex Key: {key_hex}")

# Write the key to a file
with open("key.hex", "w") as file:
    file.write(key_hex)

print("Saved to file -> key.hex")