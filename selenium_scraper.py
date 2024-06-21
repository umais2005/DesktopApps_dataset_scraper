import re

# List of words to search for
words = ["operating", "system", "memory", "ram", "hard", "disk", "space", "processor", "intel"]

# Create a regex pattern that matches any of the words
pattern = re.compile(r'\b(?:' + '|'.join(["operating", "system",
                                          "memory", "ram", "hard", "disk", "space", "processor", "intel"]) + r')\b'
                     , re.IGNORECASE)

# Example string to search in
text = "Operating System: Windows 7/8/10"

# Search for the words in the text
matches = pattern.findall(text)
print()

# Check if any matches were found
if matches:
    print("The string contains the following words:", matches)
else:
    print("None of the specified words were found in the string.")
import time
import sys
sys.exit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Setup the WebDriver

url = "https://getintopc.com/"  # Update to the target URL
driver.get(url)

# Wait for the page to fully load
driver.implicitly_wait(10)

# Get the full HTML of the page
html_content = driver.page_source

# Save the HTML content to a file
with open('page_content.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# Close the WebDriver
driver.quit()

print("HTML content successfully fetched and saved to 'page_content.html'.")
