#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import argparse
import os

parent_dir = "."
mode = 0o666

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", help="Recursively downloads the images in a URL received as a parameter, default = 5", action="store_true")
    parser.add_argument("-rl", help="Indicates the maximum depth level of the recursive download. If not indicated, 5.", type=int)
    parser.add_argument("-l", help="Indicates the maximum depth level of the recursive download. If not indicated, 5.", type=int)
    parser.add_argument("-p", help="Indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.", type=str)
    parser.add_argument("URL", help="URL", type=str)
    args = parser.parse_args()
    
    if args.r:
        print(f"-r: {args.r}")
    if args.rl:
        print(f"-rl: {args.rl}")
    if args.r and args.l:
        print(f"-rl: {args.l}")
    if args.p:
        print(f"-p: {args.p}")
        if not args.p.startswith("."):
            args.p = parent_dir + args.p
        print(f"-p: {args.p}")  
    else:
        args.p = "./data"
    if not os.path.exists(args.p):
        os.mkdir(args.p, mode)
    else: print("sorry, no")  
    print(f"Website: {args.URL}")


if __name__ == "__main__":
    main()


#-r : recursively downloads the images in a URL received as a parameter.
#-r -l [N] : indicates the maximum depth level of the recursive download.If not indicated, it will be 5.
#-p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
#The program will download the following extensions by default: .jpg/jpeg .png .gif .bmp