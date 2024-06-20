import time

import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://www.google.com/')
driver.maximize_window()
time.sleep(5)

global HEADERS 
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en-GB;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
}

# First we will defin function to scrape links from each page 
def get_page_data(page_number):
    print("Fetching Apps from page")
    URL = f'https://getintopc.com/softwares/page/{page_number}/'
    response = requests.get(URL, headers=HEADERS)
    # response.encoding = response.apparent_encoding
    # print(response.encoding)
    # print(response.text)

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
    
    
    # unfiltered = zip(names, links, categories)
    # filtered = [item for item in unfiltered if item[2].lower() not in ('tutorials', 'reviews')]
    
    # names = [item[0] for item in filtered]
    # links = [item[1] for item in filtered]
    # categories = [item[2] for item in filtered]
    # print(categories)
    return names, links, categories

def get_app_info(app_link):
    URL = app_link
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    try:
        div_content = soup.find('div', {'class', 'post-content clear-block'})
        print(div_content)
        ps_in_content = div_content.select('h2 ~ p')
    except AttributeError as e:
        print('Error occured')
        return None

    print((len(ps_in_content)))
    names = ['overview:', "desc:", 'features:', 'setup details', 'download']
    n = 0
    page_text = []
    for i in range(len(ps_in_content)):
        p = ps_in_content[i]
        if p.text:
            n+=1
            print(n)
            print(names[n-1])
            print(p.text)
            page_text.append(p.text)
        if n == len(names): break


def main():
    page_number = 322
    while True:
        names, links, categories = get_page_data(page_number)
        for name, link, cat in zip(names[1:], links[1:], categories[1:]):
            print(name)
            get_app_info(link)
            break
        break

# if __name__ == '__main__':
#     print("Sd")
#     main()