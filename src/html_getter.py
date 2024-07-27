import logging
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup


def fetch_html_with_requests(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None


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
        page.goto(url, wait_until = 'networkidle', timeout=60000)
        # Get the full HTML content of the page
        html_content = page.content()

        # Close browser
        browser.close()
        return html_content

if __name__ == '__main__':
    for page in range(1):
        html_content = fetch_html_with_requests(f"https://getintopc.com/softwares/page/{page}/")
        # print(html_content)
        # if html_content:
        #     # process_page(page)
        # else:
        #     print("Failed to fetch HTML content.")