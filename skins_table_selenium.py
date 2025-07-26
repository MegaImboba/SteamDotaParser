from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

URL = "https://new.skins-table.xyz/?g=570&n=Inscribed&pf1=&pt1=&pf2=&pt2=&cif1=1&cit1=&cif2=1&cit2=&fit1=&fit2=&bd1=8&bd2=8&pf=&pt=&csd=0&csb=0&css=0&csbs=0&csm=0&ss1=STEAM&ss2=STEAM+ORDER&sb=ON&ob=ON&fb=OFF&stb=ON&scb=ON&nb=OFF&mi=OFF&pb=ON&cs=USD"


def open_skins_table():
    options = EdgeOptions()
    options.add_argument('--start-maximized')
    # Uncomment the next line to run headless (no browser window)
    # options.add_argument('--headless')
    try:
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        driver.get(URL)
        print(f"Opening {URL}")
        wait = WebDriverWait(driver, 20)

        # Find all inputs with the class
        inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input._2GBWeup5cttgbTw8FM3tfx')))
        # There may be two: one for username, one for password
        if len(inputs) >= 2:
            # First is username, second is password
            inputs[0].clear()
            inputs[0].send_keys('LOGIN')
            inputs[1].clear()
            inputs[1].send_keys('PASSWORD')
            print("Filled in username and password.")
        else:
            print("Could not find both username and password fields.")

        time.sleep(1)

        # Find and click the submit button
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.DjSvCZoKKfoNSmarsEcTS[type="submit"]')))
        button.click()
        print("Clicked the login button.")

        # Wait 10 seconds before next action
        time.sleep(10)

        # Find and click the second login button (input)
        second_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.btn_green_white_innerfade[type="submit"]#imageLogin')))
        second_btn.click()
        print("Clicked the second login button.")

        # Wait a bit to see the result
        time.sleep(2)
        driver.get(URL)
        time.sleep(2)

        # Click the PERCENT button (span with id='percent')
        percent_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span#percent')))
        percent_btn.click()
        print("Clicked the PERCENT button.")
        time.sleep(2)

        # Extract only the text of all elements with class 'team-meta__name' in tbody[name='table']
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        tbody = soup.find('tbody', {'name': 'table'})
        if tbody:
            names = [el.get_text(strip=True) for el in tbody.find_all(class_='team-meta__name')]
            with open('data.txt', 'w', encoding='utf-8') as f:
                for name in names:
                    f.write(name + '\n')
            print(f"Saved {len(names)} team-meta__name entries to data.txt.")
        else:
            print("tbody with name='table' not found.")

        time.sleep(10)
        driver.quit()
    except Exception as e:
        print(f"Error: {e}")

def main():
    open_skins_table()

if __name__ == "__main__":
    main() 
