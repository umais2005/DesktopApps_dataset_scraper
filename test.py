import asyncio
import re
import numpy as np
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def fetch_html_with_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            ignore_https_errors=True
        )

        async with context:
            page = await context.new_page()

            # Route to block unnecessary resources (images, stylesheets, fonts)
            await page.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "stylesheet", "font"] else route.continue_())

            # Navigate to the URL and wait for network idle
            await page.goto(url, wait_until='networkidle')

            # Get the full HTML content of the page
            html_content = await page.content()

        await browser.close()
        return html_content

async def get_page_data(page_number):
    url = f'https://getintopc.com/softwares/page/{page_number}/'
    page_html_content = await fetch_html_with_playwright(url)
    soup = BeautifulSoup(page_html_content, 'html.parser')

    a_tags = soup.find_all('a', attrs={'class', 'post-thumb'})
    links = [link['href'] for link in a_tags]
    categories = []

    divs_post_info = await soup.find_all('div', {'class':'post-info'})
    for div in divs_post_info:
        cat_a_tags =  await div.find_all('a', attrs={'rel':'tag'})
        categories.append(", ".join([cat.string for cat in cat_a_tags]))

    print(f"Fetching Apps from page {page_number}")
    return  links, categories

async def get_app_info(app_link, app_category):
    html = await fetch_html_with_playwright(app_link)
    soup = BeautifulSoup(html, 'html.parser')

    try:
        div_content = soup.find('div', {'class': 'post-content clear-block'})
        ps_in_content = div_content.select('h2 ~ p')

        # Description
        page_text = [p.text for p in ps_in_content if len(p.text) > 250]
        app_desc = " ".join(page_text)
        description_dict = {'desc': app_desc}

        # Features
        app_features_ul = div_content.find('ul')
        features_list = [feature.text for feature in app_features_ul.find_all('li')]
        features_text = " ".join(features_list)
        features_dict = {'features': features_text}

        # Details
        app_details_ul = app_features_ul.find_next_sibling('ul')
        details_list = [detail.text.split(":", 1)[1].strip() for detail in app_details_ul.find_all('li')]
        name, setup_size, setup_type, compatibility, release, developer = details_list[:6]
        details_dict = {
            'name': name,
            'category': app_category,
            'setup_size': setup_size,
            'setup_type': setup_type,
            'compatibility': compatibility,
            'release': release,
            'developer': developer
        }

        # Requirements
        requirements_ul = app_details_ul.find_next_sibling('ul')
        requirements_list = [requirement.text.split(":")[-1].strip() for requirement in requirements_ul.find_all('li')]
        operating_system, memory, hdd_space, cpu = requirements_list[:4]
        requirements_dict = {
            'operating_system': operating_system,
            'memory': memory,
            'hdd_space': hdd_space,
            'cpu': cpu
        }

        app_dict = {**description_dict, **features_dict, **details_dict, **requirements_dict}
        print(f"Fetched app: {details_dict['name']}")

        return app_dict

    except AttributeError as e:
        print(f"Error processing app: {app_link}")
        return None

async def process_page(page_number):
    links, categories = get_page_data(page_number)
    print("Page Fetched {}\n".format('Success' if bool(links) else "Failed"))

    if bool(links):
        apps = []
        for link, cat in zip(links, categories):
            app_dict = await get_app_info(link, cat)
            if app_dict:
                apps.append(app_dict)

        return apps

    return []

async def main():
    PAGE_RANGE = range(1, 3)  # Adjust PAGE_RANGE according to your needs

    all_apps = []
    for page_number in PAGE_RANGE:
        apps = await process_page(page_number)
        all_apps.extend(apps)

    # Do something with all_apps
    print("All apps:", all_apps)

if __name__ == "__main__":
    asyncio.run(main())
