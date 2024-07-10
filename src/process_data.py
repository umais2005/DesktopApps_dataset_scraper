from bs4 import BeautifulSoup
from  html_getter import fetch_html_with_playwright
from utils import  save_json
import numpy as np
import re
import concurrent.futures
import logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format of the log messages
    handlers=[
        logging.FileHandler('../data/logging/app.log'),  # Log to a file
        logging.StreamHandler()          # Log to the console
    ]
)


# First we will define function to scrape links from each page
def get_page_links(page_number):
    logging.info("Fetching app links from page {}".format(page_number))
    url = f'https://getintopc.com/softwares/page/{page_number}/'
    page_html_content = fetch_html_with_playwright(url)
    soup = BeautifulSoup(page_html_content, 'html.parser')

    a_tags = soup.find_all('a', attrs={'class', 'post-thumb'})
    links = [link['href'] for link in a_tags]
    imgs = [a_tag.find('img') for a_tag in a_tags]
    img_links = [img['src'] for img in imgs]

    categories = []
    divs_post_info = soup.find_all('div', {'class':'post-info'})
    for div in divs_post_info:
        cat_a_tags = div.find_all('a', attrs={'rel':'tag'})
        categories.append((", ".join([cat.string for cat in cat_a_tags])))
    try:
        assert bool(links) == True
    except AssertionError:
        logging.warning(f'No links found for page {page_number}')
    else:
        logging.info("Page {} Fetched {}".format(page_number, 'Success' if bool(links) else "Failed"))
        print(len(img_links))
    return links, categories, img_links


def get_app_info(app_link, app_category, img_link): # Scrapes app details from app page
    html = fetch_html_with_playwright(app_link)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    try:
        div_content = soup.find('div', {'class', 'post-content clear-block'})
        ps_in_content = div_content.select('h2 ~ p')

        # This is for the description of the desktop app
        page_text = [p.text for p in ps_in_content if len(p.text) > 250]
        app_desc = " ".join(page_text).strip()
        description_dict = dict(desc= app_desc)

        # This is for the features
        app_features_ul = div_content.find('ul')
        features_list = [feature.text for feature in app_features_ul.find_all('li')]
        features_text = " ".join(features_list).strip()
        features_dict = dict(features=features_text)

        # For details
        app_details_ul = app_features_ul.find_next_sibling('ul')
        details_li = app_details_ul.find_all('li')
        domain_name_regex = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+)(?:\.[a-zA-Z]{2,}){1,2}'
        details = []
        for detail in details_li:
            link = detail.find('a')
            if link:
                if link.text.lower() != "homepage":
                    developer = link.text
                else:
                    developer = (re.findall(domain_name_regex, detail.find('a').get('href')))[0]
                details.append(developer)
            else:
                detail = (detail.text.split(":",1)[-1].strip())
                details.append(detail)

        # details = [detail.text.split(":",1)[-1].strip() for detail in details_li]
        app_details = details[:1] + details[2:]
        try:
            assert len(app_details) == 6
        except AssertionError:
            if len(app_details) < 6: # Making sure details match with names
                app_details = app_details + [None] * (6 - len(app_details))
            elif len(app_details) > 6:
                app_details = app_details[:6]
        finally:
            name, setup_size, setup_type, compatibility, release, developer = app_details
        details_dict = dict(name=name,
                            category=app_category,
                            developer=developer,
                            release=release,
                            setup_size=setup_size,
                            setup_type=setup_type,
                            compatibility=compatibility,
                            )
        
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
            app_requirements = [requirement.split(":")[-1].strip() for requirement in app_requirements]

        operating_system, ram_required, hdd_space, cpu = app_requirements
        requirements_dict = dict(operating_system=operating_system,
                                 ram_required=ram_required,
                                 hdd_space=hdd_space,
                                 cpu=cpu,
                                 img_link=img_link
                                 )
        app_dict = details_dict | requirements_dict | description_dict | features_dict
        n_items = len([item for item in list(app_dict.values()) if item])
        logging.debug(f"fetched {n_items} out of 14 for {name}")
    except Exception as e:
        # To see what's wrong with the html that is causing errors
        logging.error(f"fetching app details failed: {e}")
        return None
    return app_dict


def process_page(page_number):
    page_apps = []
    links, categories, img_links = get_page_links(page_number)
    if bool(links):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda link, cat, img_link: page_apps.append(get_app_info(link, cat, img_link)), links, categories, img_links)
    filename = save_json([page_app for page_app in page_apps if page_app], page_number, by_page=True)
    if filename: logging.info(f"Data successfully written to {filename}\n")
    # returns list of dicts
    return page_apps


if __name__ == '__main__':
    # print(get_app_info(r'https://getintopc.com/softwares/music/atomix-virtualdj-pro-infinity-portable-free-download/'))
    # app, cat, link = get_page_links(1)
    # get_app_info(app[0], cat[0], link[0])
    process_page(1)