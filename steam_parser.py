import os
import re
import json
import time
import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import random



class SteamMarketParser:
    def __init__(self, data_file: str = 'steamdata.txt', output_file: str = 'to_buy.txt', cookies_file: str = 'cookies.json'):
        self.data_file = data_file
        self.output_file = output_file
        self.cookies_file = cookies_file
        self.mod_data: List[str] = []
        self.results: Dict[str, Any] = {}
        self.base_url = 'https://steamcommunity.com/market/listings/570/'
        self.histogram_url = 'https://steamcommunity.com/market/itemordershistogram?'
        self.cookies = self.load_cookies()

    def load_cookies(self) -> Dict[str, str]:
        if not os.path.exists(self.cookies_file):
            print(f"Warning: {self.cookies_file} not found. No cookies will be used.")
            return {}
        with open(self.cookies_file, 'r', encoding='utf-8') as f:
            cookies_list = json.load(f)
        cookies = {}
        for cookie in cookies_list:
            if cookie.get('domain') and 'steamcommunity.com' in cookie['domain']:
                cookies[cookie['name']] = cookie['value']
        return cookies

    def load_and_clean_data(self):
        if not os.path.exists(self.data_file):
            print(f"File {self.data_file} not found. Please add it and rerun.")
            return
        with open(self.data_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                cleaned = re.sub(r'^(Inscribed|Autographed)\s+', '', line)
                if cleaned:
                    self.mod_data.append(cleaned)

    def fetch_item_data(self):
        for item in self.mod_data:
            versions = {
                'Standard': item,
                'Inscribed': f'Inscribed {item}',
                'Autographed': f'Autographed {item}'
            }
            self.results[item] = {}
            # Track if item_nameid was found in DotaNameID.txt for all qualities
            item_in_nameid_file = True
            for quality, name in versions.items():
                # Check if name is already in DotaNameID.txt
                nameid_file = 'DotaNameID.txt'
                item_nameid = None
                if os.path.exists(nameid_file):
                    with open(nameid_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.startswith(f"{name} - "):
                                # Extract nameid from the line
                                try:
                                    item_nameid = line.strip().split(' - ')[1]
                                except Exception as e:
                                    print(f"Error parsing nameid from {nameid_file}: {e}")
                                break
                if not item_nameid:
                    item_in_nameid_file = False
                    url = self.base_url + requests.utils.quote(name)
                    try:
                        resp = requests.get(url, cookies=self.cookies)
                        if resp.status_code != 200:
                            print(f"Failed to fetch {name}: HTTP {resp.status_code}")
                            continue
                        # Parse the HTML and look for <script type="text/javascript"> containing Market_LoadOrderSpread
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        scripts = soup.find_all('script', {'type': 'text/javascript'})
                        for script in scripts:
                            if script.string and 'Market_LoadOrderSpread' in script.string:
                                match = re.search(r'Market_LoadOrderSpread\s*\(\s*(\d+)\s*\)', script.string)
                                if match:
                                    item_nameid = match.group(1)
                                    # Save to DotaNameID.txt if not already present
                                    line_to_write = f"{name} - {item_nameid}\n"
                                    try:
                                        exists = False
                                        if os.path.exists(nameid_file):
                                            with open(nameid_file, 'r', encoding='utf-8') as f2:
                                                for line2 in f2:
                                                    if line2.startswith(f"{name} - "):
                                                        exists = True
                                                        break
                                        if not exists:
                                            with open(nameid_file, 'a', encoding='utf-8') as f2:
                                                f2.write(line_to_write)
                                    except Exception as e:
                                        print(f"Error writing to {nameid_file}: {e}")
                                    break
                    except Exception as e:
                        print(f"Error processing {name}: {e}")
                        continue
                if not item_nameid:
                    print(f"item_nameid not found for {name}")
                    continue
                params = {
                    'country': 'MD',
                    'language': 'english',
                    'currency': 1,
                    'item_nameid': item_nameid
                }
                hist_resp = requests.get(self.histogram_url, headers=self._headers, params=params, cookies=self.cookies)
                if hist_resp.status_code != 200:
                    print(f"Failed to fetch histogram for {name}")
                    continue
                hist_data = hist_resp.json()
                # Ensure None values are set to 0
                lowest_sell_order = hist_data.get('lowest_sell_order', 0)
                highest_buy_order = hist_data.get('highest_buy_order', 0)
                if lowest_sell_order is None:
                    lowest_sell_order = 0
                if highest_buy_order is None:
                    highest_buy_order = 0
                self.results[item][quality] = {
                    'item_nameid': item_nameid,
                    'lowest_sell_order': int(lowest_sell_order),
                    'highest_buy_order': int(highest_buy_order)
                }
                # Remove per-quality sleep
            # After all qualities for this item, sleep accordingly
            if item_in_nameid_file:
                time.sleep(1)
            else:
                time.sleep(random.randint(5, 10))

    def analyze_and_save(self):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for item, data in self.results.items():
                try:
                    std = data.get('Standard', {})
                    ins = data.get('Inscribed', {})
                    aut = data.get('Autographed', {})
                    std_price = std.get('lowest_sell_order', 0)
                    std_buy = std.get('highest_buy_order', 0)
                    ins_price = ins.get('lowest_sell_order', 0)
                    ins_buy = ins.get('highest_buy_order', 0)
                    aut_price = aut.get('lowest_sell_order', 0)
                    aut_buy = aut.get('highest_buy_order', 0)
                    # Ensure None values are set to 0
                    std_price = ins_price if std_price is None else std_price
                    std_buy = ins_price if std_buy is None else std_buy
                    ins_price = std_price if ins_price is None else ins_price
                    ins_buy = std_price if ins_buy is None else ins_buy
                    aut_price = std_price if aut_price is None else aut_price
                    aut_buy = std_price if aut_buy is None else aut_buy
                    if std_price + 3 < ins_buy * 0.85:
                        f.write(f"[1] {item}: Standard +3 < Inscribed buy\n")
                    if ins_price < std_buy * 0.85:
                        f.write(f"[2] {item}: Inscribed < Standard buy\n")
                    if std_price + 13 < aut_buy * 0.85:
                        f.write(f"[3] {item}: Standard +13 < Autographed buy\n")
                    if ins_price + 13 < aut_buy * 0.85:
                        f.write(f"[4] {item}: Inscribed +13 < Autographed buy\n")
                    if aut_price - 5 < ins_buy * 0.85:
                        f.write(f"[5] {item}: Autographed -5 < Inscribed buy\n")
                    if aut_price - 5 < std_buy * 0.85:
                        f.write(f"[6] {item}: Autographed -5 < Standard buy\n")
                except Exception as e:
                    print(f"Error analyzing {item}: {e}")

def main():
    parser = SteamMarketParser()
    parser.load_and_clean_data()
    if not parser.mod_data:
        print("No data loaded. Exiting.")
        return
    parser.fetch_item_data()
    parser.analyze_and_save()
    print("Analysis complete. Results saved to to_buy.txt.")

if __name__ == '__main__':
    main() 