import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import os

# Path to Edge WebDriver
EDGE_DRIVER_PATH = os.path.join('edgedriver_win64', 'msedgedriver.exe')

# URL template
URL_TEMPLATE = (
    'https://steamcommunity.com/market/search?'
    'category_570_Hero%5B%5D=any&category_570_Slot%5B%5D=any&'
    'category_570_Type%5B%5D=tag_wearable&category_570_Quality%5B%5D=tag_autographed&'
    'category_570_Rarity%5B%5D=tag_Rarity_Legendary&appid=570#p{page}_popular_desc'
)

# Load cookies from cookies.json
with open('cookies.json', 'r', encoding='utf-8') as f:
    cookies = json.load(f)

# Set up Edge options
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')

service = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

def add_cookies(driver, cookies):
    driver.get('https://steamcommunity.com')
    for cookie in cookies:
        # Selenium expects expiry as int, not float
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        # Remove fields not accepted by Selenium
        cookie.pop('sameSite', None)
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Could not add cookie: {cookie.get('name')}, error: {e}")

# Open Steam Community to set cookies
add_cookies(driver, cookies)

# Visit each page from 1 to 39
for page in range(1, 8):
    url = URL_TEMPLATE.format(page=page)
    print(f"Loading page {page}: {url}")
    driver.get(url)
    time.sleep(3)
    # Extract item names
    item_names = driver.find_elements(By.CLASS_NAME, 'market_listing_item_name')
    with open('steamdata.txt', 'a', encoding='utf-8') as f:
        for item in item_names:
            name = item.text.strip()
            if name:
                f.write(name + '\n')

print("Done. Closing browser.")
driver.quit() 