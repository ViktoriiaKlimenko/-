#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-
__author__ = 'wudaown'

import requests
from bs4 import BeautifulSoup
import os

def getSource(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()  
    except requests.RequestException as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return {}

    soup = BeautifulSoup(r.text, 'lxml')
    comic = {}
    for h2 in soup.find_all('h2'):
        if h2.contents and hasattr(h2.contents[0], 'attrs'):
            comic[h2.contents[0]['href']] = h2.contents[0]['title'][13:]
    return comic

def getPageNumber(page_url):
    try:
        p = requests.get(page_url, timeout=10)
        p.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при загрузке {page_url}: {e}")
        return [page_url]  

    soup = BeautifulSoup(p.text, 'lxml')
    page_nav = soup.find(class_='wp-pagenavi')
    if not page_nav or len(page_nav.contents) < 3:
        return [page_url] 

    last_page = page_nav.contents[-3].get_text(strip=True)
    return [f"{page_url}/{i}" for i in range(1, int(last_page) + 1)]

def downloadComic(comic_link, comic_name):
    os.makedirs(comic_name, exist_ok=True)  
    img_count = 0

    for page in getPageNumber(comic_link):
        try:
            img_links = [img['src'] for img in BeautifulSoup(
                requests.get(page).text, 'lxml'
            ).find_all('img') if 'alt' in img.attrs]
            
            for img_url in img_links:
                img_data = requests.get(img_url).content
                with open(os.path.join(comic_name, f"{img_count:03d}.jpg"), 'wb') as f:
                    f.write(img_data)
                img_count += 1
                print(f"Загружено: {img_count} стр.", end='\r')
        except Exception as e:
            print(f"Ошибка на странице {page}: {e}")

def main():
    if not os.path.exists('recode'):
        with open('recode', 'w') as f:
            f.write('1') 

    with open('recode', 'r+') as f:
        start_page = int(f.read().strip() or 1)
        base_url = 'http://www.177pic.info/html/category/tt/page/'
        
        for page_num in range(start_page, getSourcePageNumber() + 1):
            print(f"\nСтраница {page_num}:")
            f.seek(0)
            f.write(str(page_num)) 
            
            for url, name in getSource(f"{base_url}{page_num}").items():
                if not os.path.exists(f"{name}.cbr"):
                    downloadComic(url, name)
                   

if __name__ == '__main__':
    main()