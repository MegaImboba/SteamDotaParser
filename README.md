# Steam Market Selenium Scraper

This script (`steam_market_selenium.py`) uses Selenium and Edge WebDriver to scrape item names from the Steam Community Market for Dota 2 Legendary autographed wearables.

## Features
- Logs in using your Steam cookies from `cookies.json`.
- Visits pages 1 to 7 of the Legendary autographed wearables market search.
- Extracts all item names from each page and saves them to `steamdata.txt` (one per line).

## Prerequisites
- Python 3.7+
- [Selenium](https://pypi.org/project/selenium/)
- Microsoft Edge browser
- Edge WebDriver (`msedgedriver.exe`) in the `edgedriver_win64` directory
- A valid `cookies.json` file with your Steam login cookies

## Setup
1. Install dependencies:
   ```bash
   pip install selenium
   ```
2. Download the correct version of Edge WebDriver for your Edge browser and place `msedgedriver.exe` in the `edgedriver_win64` folder.
3. Place your Steam cookies in `cookies.json` (exported from your browser).

## Usage
Run the script with Python:
```bash
python steam_market_selenium.py
```

- The script will open Edge, log in using your cookies, and visit each market page.
- It will wait 3 seconds on each page, extract all item names, and append them to `steamdata.txt`.

## Notes
- Make sure your cookies are up to date and valid for Steam.
- You can adjust the number of pages or wait time by editing the script.
- The script is currently set to scrape Legendary autographed wearables. To change filters, modify the URL in the script.

## Disclaimer
This script is for educational purposes only. Use it responsibly and respect Steam's terms of service. 

## Other Scripts

### steam_parser.py
This script parses Dota 2 item data and market information using requests and BeautifulSoup. It can:
- Read item names from `data.txt`.
- Use cookies from `cookies.json` to access Steam Market pages.
- Extract `nameid` for each item and save it to `DotaNameID.txt` (avoiding duplicates).
- Use the `nameid` to fetch price and order data from the Steam Market API.
- Save analysis results to `to_buy.txt`.

**Usage:**
```bash
python steam_parser.py
```

**Requirements:**
- Python 3.7+
- requests
- beautifulsoup4
- A valid `cookies.json` file
- Input file: `data.txt` (list of item names)

### skins_table_selenium.py
This script (if present) is intended for Selenium-based scraping of Dota 2 skin tables or listings. It can be used to:
- Automate browser actions to extract tabular or listing data from the Steam Market or similar pages.
- Save extracted data for further analysis.

**Usage:**
```bash
python skins_table_selenium.py
```

**Requirements:**
- Python 3.7+
- selenium
- Microsoft Edge browser and Edge WebDriver (or modify for your browser)
- A valid `cookies.json` file (if login is required)

---

Each script is designed for a specific workflow:
- `steam_market_selenium.py`: Scrapes item names from the Steam Market using Selenium.
- `steam_parser.py`: Parses and analyzes item price/order data using requests and BeautifulSoup.
- `skins_table_selenium.py`: (If present) Automates browser to extract tabular/listing data, customizable for your needs. 