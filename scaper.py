import re
import time
import random
import asyncio
import numpy as np
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def fetch_html_with_playwright(url):
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            ignore_https_errors=True
        )

        # Disable loading images and other unnecessary resources
        context.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "stylesheet", "font"] else route.continue_())

        # Open new page
        page = context.new_page()

        # Go to the URL and wait for the network to be idle
        page.goto(url, wait_until='networkidle')

        # Get the full HTML content of the page
        html_content = page.content()

        # Close browser
        browser.close()
        return html_content
async def fetch_multiple_pages(urls):
    tasks = [fetch_html_with_playwright(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def fetch_multiple_pages(links):
    tasks = [get_app_info(link) for link in links]
    page_results = await asyncio.gather(*tasks)
    return page_results

def save_html(html_content):
    with open('page_content.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
        file.close()

# global HEADERS
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en-GB;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
}

# First we will defin function to scrape links from each page
def get_page_data(page_number):
    url = f'https://getintopc.com/softwares/page/{page_number}/'
    page_html_content = fetch_html_with_playwright(url)
    soup = BeautifulSoup(page_html_content, 'html.parser')

    a_tags = soup.find_all('a', attrs={'class', 'post-thumb'})
    links = [link['href'] for link in a_tags]
    categories = []

    divs_post_info = soup.find_all('div', {'class':'post-info'})
    for div in divs_post_info:
        cat_a_tags = div.find_all('a', attrs={'rel':'tag'})
        categories.append((", ".join([cat.string for cat in cat_a_tags])))
    # print(names)
    print("Fetching Apps from page{}".format(page_number))
    return links, categories

def get_app_info(app_link, app_category):
    html = fetch_html_with_playwright(app_link)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    try:                                    #class="post-content clear-block"
        div_content = soup.find('div', {'class', 'post-content clear-block'})
        ps_in_content = div_content.select('h2 ~ p')

        # This is for the description of the desktop app
        page_text = [p.text for p in ps_in_content if len(p.text) > 250]
        app_desc = " ".join(page_text)
        description_dict = dict(desc= app_desc)
        # This is for the features
        app_features_ul = div_content.find('ul')
        features_list = [feature.text for feature in app_features_ul.find_all('li')]
        features_text = " ".join(features_list)
        features_dict = dict(features=features_text)

        # For details
        app_details_ul = app_features_ul.find_next_sibling('ul')
        details_list = [detail.text.split(":",1)[1] for detail in app_details_ul.find_all('li')]
        app_details = details_list[:1] + details_list[2:] + ['d']
        try:
            assert len(app_details) == 6
        except AssertionError:
            if len(app_details) < 6: # Making sure details match with names
                app_details = app_details + [np.nan] * (6 - len(app_details))
            elif len(app_details) > 6:
                app_details = app_details[:6]
        finally:
            name, setup_size, setup_type, compatibility, release, developer = app_details
        print(name, setup_size, setup_type, compatibility, release, developer)
        details_dict = dict(name=name,
                            category=app_category,
                            setup_size=setup_size,
                            setup_type=setup_type,
                            compatibility=compatibility,
                            release=release,
                            developer=developer)
        # For System requirements
        pattern = re.compile(r'\b(?:' + '|'.join(["operating", "system",
                                                  "memory", "ram", "hard", "disk", "space", "processor",
                                                  "intel"]) + r')\b', re.IGNORECASE)
        try:
            requirements_ul = app_details_ul.find_next_sibling('ul')
            assert bool(requirements_ul) == True
        except AssertionError:
            app_requirements = [np.nan] * 4
        else:
            app_requirements = [requirement.text for requirement in requirements_ul.find_all('li')]
            app_requirements = [requirement.split(":")[-1] for requirement in app_requirements]
        operating_system, memory, hdd_space, cpu = app_requirements
        requirements_dict = dict(operating_system=operating_system,
                                 memory=memory,
                                 hdd_space=hdd_space,
                                 cpu=cpu)
        app_dict = description_dict | features_dict | requirements_dict | details_dict
        # print("{} Saved details for {}".format(app_dict.keys(),name))
        return app_dict
    except AttributeError as e:
        save_html(html) # To see what's wrong with the html that is causing errors
        print("Error")
        return
        # return

def main():
    for page_number in range(32, 35):
        links, categories = get_page_data(page_number)
        # print(asyncio.run(fetch_multiple_pages(links)))
        print("Page Fetched {}\n".format('Success' if bool(links) else "Failed"))
        if bool(links):
            for link, cat in zip(links, categories):
                app_dict = get_app_info(link, cat)
                n_items = len([item for item in list(app_dict.values()) if item])
                # print(list(app_dict.values())[2:])
                print(f"fetched {n_items} out of 13")


if __name__ == '__main__':
    main()
    # (get_app_info('https://getintopc.com/softwares/backup-recovery/advik-gmail-backup-enterprise-2022-free-download/'))
    # page_number = 4
    # URL = f'https://getintopc.com/softwares/page/{page_number}/'
    # html_content = fetch_html_with_playwright(URL)
    #
    # # Save the HTML content to a file
    # with open('page_content.html', 'w', encoding='utf-8') as file:
    #     file.write(html_content)
    #
    # print("HTML content successfully fetched and saved to 'page_content.html'.")