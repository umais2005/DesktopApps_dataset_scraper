import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://getintopc.com/softwares/')
time.sleep(2)
