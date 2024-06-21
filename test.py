import re
import asyncio
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

        await context.route("**/*",
                            lambda route, request: route.abort() if request.resource_type in ["image", "stylesheet",
                                                                                              "font"] else route.continue_())

        page = await context.new_page()
        await page.goto(url, wait_until='networkidle')

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

    divs_post_info = soup.find_all('div', {'class': 'post-info'})
    for div in divs_post_info:
        cat_a_tags = div.find_all('a', attrs={'rel': 'tag'})
        categories.append(", ".join([cat.string for cat in cat_a_tags]))

    print(f"Fetching Apps from page {page_number}")
    return links, categories


async def get_app_info_async(app_link, app_category):
    html = await fetch_html_with_playwright(app_link)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        div_content = soup.find('div', {'class', 'post-content clear-block'})
        ps_in_content = div_content.select('h2 ~ p')

        page_text = [p.text for p in ps_in_content if len(p.text) > 250]
        app_desc = " ".join(page_text)
        description_dict = dict(desc=app_desc)

        app_features_ul = div_content.find('ul')
        features_list = [feature.text for feature in app_features_ul.find_all('li')]
        features_text = " ".join(features_list)
        features_dict = dict(features=features_text)

        app_details_ul = app_features_ul.find_next_sibling('ul')
        details_list = [detail.text.split(":", 1)[1] for detail in app_details_ul.find_all('li')]
        app_details = details_list[:1] + details_list[2:] + ['d']
        if len(app_details) < 6:
            app_details = app_details + [np.nan] * (6 - len(app_details))
        elif len(app_details) > 6:
            app_details = app_details[:6]

        name, setup_size, setup_type, compatibility, release, developer = app_details
        details_dict = dict(
            name=name,
            category=app_category,
            setup_size=setup_size,
            setup_type=setup_type,
            compatibility=compatibility,
            release=release,
            developer=developer
        )

        pattern = re.compile(r'\b(?:' + '|'.join(
            ["operating", "system", "memory", "ram", "hard", "disk", "space", "processor", "intel"]) + r')\b',
                             re.IGNORECASE)
        try:
            requirements_ul = app_details_ul.find_next_sibling('ul')
            assert bool(requirements_ul) == True
        except AssertionError:
            app_requirements = [np.nan] * 4
        else:
            app_requirements = [requirement.text for requirement in requirements_ul.find_all('li')]
            app_requirements = [requirement.split(":")[-1] for requirement in app_requirements]
        operating_system, memory, hdd_space, cpu = app_requirements
        requirements_dict = dict(
            operating_system=operating_system,
            memory=memory,
            hdd_space=hdd_space,
            cpu=cpu
        )
        app_dict = description_dict | features_dict | requirements_dict | details_dict
        return app_dict
    except AttributeError as e:
        print("Error")
        return


async def process_page(page_number):
    links, categories = await get_page_data(page_number)
    print(f"Page Fetched {'Success' if bool(links) else 'Failed'}\n")

    if links:
        tasks = [get_app_info_async(link, cat) for link, cat in zip(links, categories)]
        app_dicts = await asyncio.gather(*tasks)

        for app_dict in app_dicts:
            if app_dict:
                n_items = len([item for item in list(app_dict.values()) if item])
                print(f"fetched {n_items} out of 13")


async def main():
    tasks = [process_page(page_number) for page_number in range(32,35)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
