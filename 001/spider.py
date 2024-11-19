#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import argparse
import os
from typing import List
from urllib.parse import urljoin

parser = argparse.ArgumentParser()
parser.add_argument("-r", help="Recursively downloads the images in a URL received as a parameter, default = 5", action="store_true")
parser.add_argument("-l", help="Indicates the maximum depth level of the recursive download. If not indicated, 5.", type=int, default = 5)
parser.add_argument("-p", help="Indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.", default = "./data", type=str)
parser.add_argument("URL", help="URL", type=str)
args = parser.parse_args()

def recursive_url(url, link, depth) -> List[str]:
    if depth == args.l:
        return url
    
    if 'href' not in link.attrs:
        return []

    print(f"Link: {link['href']}")

    link_url = link['href']
    if link_url.startswith('//'):
        link_url = 'https:' + link_url
    full_url = urljoin(url, link_url)
    print(f'Full url: {full_url}')

    try:
        response = requests.get(full_url)
    except requests.exceptions.RequestException as e:
        print(e)
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    new_links = soup.find_all('a', href=True)

    imgs = find_imgs(full_url)

    for new_link in new_links:
        imgs += recursive_url(url, new_link, depth + 1)

    return imgs


def get_links(url: str) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    return links

def download_img(img: str, folder: str) -> None:
    response = requests.get(img, stream = True)
    if response.status_code == 200:
        filename = folder + '/' + os.path.basename(img)
        # print (filename)
        with open(filename, 'wb') as file:
            file.write(response.content)

def find_imgs(url: str) -> List[str]:
    try:
        response = requests.get(url)
        print (f"Status code: {response.status_code}")
        # print (response)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print (soup.prettify())
        imgs = [img['src'] for img in soup.find_all('img') if img['src'].endswith(('.jpg', 'jpeg', '.png', 'gif', 'bmp'))]
        return imgs
    except Exception as e:
        print (f"An error occured: {e}")
        return []

def main():
    
    if not os.path.exists(args.p):
        os.mkdir(args.p, 0o777) 
    print(f"Website: {args.URL}")

    imgs = []
    if (args.r):
        links = get_links(args.URL)
        for link in links:
            imgs += recursive_url(args.URL, link, 0)
    else:
        imgs = find_imgs(args.URL)

    print (f'Downloadint images to {args.p}...')
    for img in imgs:
        download_img(img, args.p)
    print ('Done!')


if __name__ == "__main__":
    main()


#-r : recursively downloads the images in a URL received as a parameter.
#-r -l [N] : indicates the maximum depth level of the recursive download.If not indicated, it will be 5.
#-p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
#The program will download the following extensions by default: .jpg/jpeg .png .gif .bmp