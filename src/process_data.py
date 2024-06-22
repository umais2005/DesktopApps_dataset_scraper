from bs4 import BeautifulSoup
from  html_getter import fetch_html_with_playwright
from utils import save_html, save_json
import numpy as np
import re
import concurrent.futures


# First we will define function to scrape links from each page
def get_page_links(page_number):
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


def get_app_info(app_link, app_category): # Scrapes app details from app page
    html = fetch_html_with_playwright(app_link)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    try:
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
                                 )
        app_dict = details_dict | requirements_dict | description_dict | features_dict
        n_items = len([item for item in list(app_dict.values()) if item])
        print(f"fetched {n_items} out of 13 for {name}")
        return app_dict
    except AttributeError as e:
        save_html(html) # To see what's wrong with the html that is causing errors
        print("Error")
        return


def process_page(page_number):
    page_apps = []
    links, categories = get_page_links(page_number)
    print("Page {} Fetched {}\n".format(page_number, 'Success' if bool(links) else "Failed"))
    if bool(links):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda link, cat: page_apps.append(get_app_info(link, cat)), links, categories)

    save_json(page_apps, page_number, by_page=True)
    # returns list of dicts
    return page_apps
