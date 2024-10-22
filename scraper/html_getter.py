import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


# def fetch_html_with_playwright(url):
#     with sync_playwright() as p:
#         # Launch the browser
#         browser = p.chromium.launch(headless=True)
#         context = browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             viewport={"width": 1280, "height": 800},
#             ignore_https_errors=True
#         )

#         # Disable loading images and other unnecessary resources
#         context.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "stylesheet", "font"] else route.continue_())

#         # Open new page
#         page = context.new_page()
#         # Go to the URL and wait for the network to be idle
#         page.goto(url, wait_until = 'networkidle', timeout=60000)
#         # Get the full HTML content of the page
#         html_content = page.content()

#         # Close browser
#         browser.close()
#         return html_content
    
def fetch_html_with_selenium(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # To prevent detection
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore HTTPS errors

    # Set user-agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    # Launch the browser
    driver = webdriver.Chrome( options=chrome_options)

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load completely using network idle-like conditions
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'body'))
        )

        # Get the full HTML content of the page
        html_content = driver.page_source

    finally:
        # Close the browser
        driver.quit()
    
    return html_content


if __name__ == '__main__':
    for page in range(1):
        html_content = fetch_html_with_requests(f"https://getintopc.com/softwares/page/{page}/")
        # print(html_content)
        # if html_content:
        #     # process_page(page)
        #     print("Failed to fetch HTML content.")