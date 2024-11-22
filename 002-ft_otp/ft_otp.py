#!/usr/bin/env python3

import argparse
import hmac
import hashlib
import struct
import time
import base64

parser = argparse.ArgumentParser()
parser.add_argument("-g", help="A hexadecimal key of at least 64 characters is required, .hex file")
parser.add_argument("-k", help="to generate a new temporary password, takes a .key file")    
args = parser.parse_args()

def ft_hotp(key: str, time_counter: int) -> int:

    key_bytes = bytes.fromhex(key) #Convert hex to bytes
    print (f'key_bytes: {key_bytes}')

    counter_bytes = struct.pack(">Q", time_counter)  #Convert counter to bytes
    print (f'counter_bytes: {counter_bytes}')

    hmac_hash = hmac.new(key_bytes, counter_bytes, hashlib.sha1).digest() #Generate HMAC
    print (f'hmac_hash: {hmac_hash}')

    last_byte = hmac_hash[-1] #offset from the last byte of the hash -- where to start extracting the OTP
    print (f'last_byte: {last_byte}')

    offset = last_byte & 0x0F #The last 4 bits of the byte -- the offset
    print (f'offset: {offset}')

    offset_bytes = hmac_hash[offset:offset + 4] #Extract bytes starting at the offset
    print (f'offset_bytes: {offset_bytes}')

    unpacked_code = struct.unpack(">I", offset_bytes) #Extracting a 4-byte segment from the HMAC-SHA1 hash
    print (f'unpacked_code: {unpacked_code}')

    binary_code = unpacked_code[0] #take the first element
    print (f'binary_code: {binary_code}')
    
    otp = binary_code & 0x7FFFFFFF #Make a positive number
    print (f'full otp: {otp}')

    otp = otp % 1000000 # to have only 6 digits

    return otp



def open_and_check_file(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            key = file.read().strip()
            print (key)
        if len(key) != 64:
            raise ValueError("Error: key must have 64 characters.")
        if not all(c in '0123456789abcdefABCDEF' for c in key):
            print("Error: Key must be hexadecimal.")
        return (key)
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
    except ValueError as e:
        print(f"Error: {e}")
    return None

def main():
    if args.g:
        print("\nExtracting and saving key...\n")
        key = open_and_check_file(args.g)
        if key is None:
            return
        key_base32 = base64.b32encode(bytes.fromhex(key)).decode('utf-8') # -> to base 32
        with open("ft_otp.key", "w") as file:
            file.write(key_base32)
            print("Success: key was saved in ft_otp.key\n\n")

    if args.k:
        print("Generating one time password...")
        with open(args.k, "r") as file:
            encoded_key = file.read().strip()
        hex_key = base64.b32decode(encoded_key).hex()
        print (f'Hex_key: {hex_key}')
        time_counter = int(time.time() // 30)
        print (f'Time counter: {time_counter}')
        one_time_pass = ft_hotp(hex_key, time_counter)
        print (f'\n---\nOne time password: {one_time_pass}\n---\n')

if __name__ == '__main__':
    main()