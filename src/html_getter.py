import logging
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
        page.goto(url, wait_until = 'networkidle')
        # Get the full HTML content of the page
        html_content = page.content()

        # Close browser
        browser.close()
        return html_content
