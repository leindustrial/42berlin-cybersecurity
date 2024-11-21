#!/usr/bin/env python3

import os

key = os.urandom(32).hex()

print(f"Generated Key: {key}")

# Write the key to a file
with open("key.hex", "w") as file:
    file.write(key)

print("Saved to file -> key.hex")