#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import argparse
import os
from typing import List
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from urllib.parse import urlparse
import tldextract

filecount = 0
filecount_lock = Lock()
visited_links = set()

parser = argparse.ArgumentParser()
parser.add_argument("-r", help="Recursively downloads the images in a URL received as a parameter, default = 5", action="store_true")
parser.add_argument("-l", help="Indicates the maximum depth level of the recursive download. If not indicated, 5.", type=int, default = 5)
parser.add_argument("-p", help="Indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.", default = "./data", type=str)
parser.add_argument("URL", help="URL", type=str)
args = parser.parse_args()

def recursive_url(url, link, depth) -> List[str]:
    if depth >= args.l:
        return []
    
    if 'href' not in link.attrs:
        return []

    link_url = link['href']
    if link_url == '#' or not link_url.strip():
        return []
    
    if not link_url.startswith(('http://', 'https://')):
        parsed = urlparse(link_url)
        if parsed.scheme not in ['http', 'https']:
            return []
        
    if link_url.startswith('//'):
        link_url = 'https:' + link_url
    full_url = urljoin(url, link_url)

    # full_url = urljoin(url, link_url)
    # parsed_base = urlparse(url)
    # parsed_link = urlparse(full_url)

    # if parsed_base.netloc != parsed_link.netloc:
    #     print(f"Skipping external link: {full_url}")
    #     return []
    base_domain = tldextract.extract(url)
    link_domain = tldextract.extract(full_url)
    if f"{base_domain.domain}.{base_domain.suffix}" != f"{link_domain.domain}.{link_domain.suffix}":
        print(f"Skipping external link: {full_url}")
        return []

    if full_url in visited_links:
        return []

    visited_links.add(full_url)

    print(f'URL found: {full_url}')

    try:
        response = requests.get(full_url, timeout=5)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs = find_imgs(full_url)
        new_links = soup.find_all('a', href=True)
        for new_link in new_links:
            imgs += recursive_url(url, new_link, depth + 1)
        return imgs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {full_url}: {e}")
        return []


def get_links(url: str) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    return links

def download_img(img: str, folder: str) -> None:
    global filecount

    if img.startswith('//'):
        img = 'https:' + img

    filename = folder + '/' + os.path.basename(img)
    if os.path.exists(filename):  # Check if the file already exists
        print(f"Skipping dublicate {filename}...")
        return
    
    try:
        response = requests.get(img, stream=True)
        if response.status_code == 200:
            filename = folder + '/' + os.path.basename(img)
            with open(filename, 'wb') as file:
                print(f'Downloading {filename}...')
                file.write(response.content)
            
            # I use lock to update the global filecount (safe with threads)
            with filecount_lock:
                filecount += 1
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {img}: {e}")

def find_imgs(url: str) -> List[str]:
    try:
        response = requests.get(url)
        # print(f"Status code: {response.status_code}\n")
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs = [
            urljoin(url, img['src'])
            for img in soup.find_all('img', src=True)
            if img['src'].endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))
        ]
        return imgs
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def download_images_concurrently(imgs: List[str], folder: str) -> None:
    with ThreadPoolExecutor(max_workers=10) as executor:
        for img in imgs:
            executor.submit(download_img, img, folder)

def main():
    

    if not os.path.exists(args.p):
        os.mkdir(args.p, 0o777) 
    print(f"Website: {args.URL}")

    imgs = []
    imgs += find_imgs(args.URL)
    if (args.r):
        links = get_links(args.URL)
        for link in links:
            imgs += recursive_url(args.URL, link, 0)
    else:
        imgs = find_imgs(args.URL)

    print (f'Downloading images to {args.p}...')
    # for img in imgs:
    #     download_img(img, args.p)
    download_images_concurrently(imgs, args.p)
    print (f'Done! Saved {filecount} images')


if __name__ == "__main__":
    main()


#-r : recursively downloads the images in a URL received as a parameter.
#-r -l [N] : indicates the maximum depth level of the recursive download.If not indicated, it will be 5.
#-p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
#The program will download the following extensions by default: .jpg/jpeg .png .gif .bmp