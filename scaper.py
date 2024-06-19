import requests
from bs4 import BeautifulSoup 
import re

global HEADERS 
HEADERS = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
# 'authority':'getintopc.com',
'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Encoding":"gzip, deflate, br, zstd",
"Accept-Language":"en-US,en-GB;q=0.9,en;q=0.8"}

# First we will defin function to scrape links from each page 
def get_page_data(page_number):
    URL = f'https://getintopc.com/page/{page_number}/?0'
    response = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())
    a_tags = soup.find_all('a', attrs={'class', 'post-thumb'})
    links = [link['href'] for link in a_tags]
    names = [name['title'] for name in a_tags]
    categories = []

    divs_post_info = soup.find_all('div', {'class':'post-info'})
    for div in divs_post_info:
        cat_a_tags = div.find_all('a', attrs={'rel':'tag'})
        categories.append((", ".join([cat.string for cat in cat_a_tags])))
    
    
    unfiltered = zip(names, links, categories)
    filtered = [item for item in unfiltered if item[2].lower() not in ('tutorials', 'reviews')]
    
    names = [item[0] for item in filtered]
    links = [item[1] for item in filtered]
    categories = [item[2] for item in filtered]
    # print(categories)
    return names, links, categories

def get_app_info(app_link):
    URL = app_link
    response = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(response.text, 'html.parser')
    div_content = soup.find_all('')

def main():
    page_number = 1
    while True:
        names, links, categories = get_page_data(page_number)
        for name, link, cat in zip(names, links, categories):
            get_app_info(link)

if __name__ == '__main__':
    main()