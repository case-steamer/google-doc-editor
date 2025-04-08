from bs4 import BeautifulSoup
import gspread
import requests

zillow_url = "https://appbrewery.github.io/Zillow-Clone/"
headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-67eeb488-2c0c32b07284239833f6c3bf"
}






def clean_data(data):
    """RETURNS cleaned data. Used inside the make_soup() function"""
    cleaned = []
    try:
        for point in data:
            if "/" in point.text:
                cleaned.append(point.text.split("/")[0])
            elif "+" in point.text:
                cleaned.append(point.text.split("+")[0])
    except:
        for point in data:
            if "/" in point:
                cleaned.append(point.split("/")[0])
            elif "+" in point:
                cleaned.append(point.split("+")[0])
            else:
                cleaned.append(point)
    return cleaned


def make_soup():
    """RETURNS SCRAPED DATA"""
    locations = []
    hrefs = []
    masters = []
    response = requests.get(url=zillow_url, headers=headers)
    try:
        zillow_page = response.text
        soup = BeautifulSoup(zillow_page, "lxml")
        addresses = soup.find_all('address')
        prices = soup.find_all(name='span', class_='PropertyCardWrapper__StyledPriceLine')
        links = soup.find_all(name='a', class_='StyledPropertyCardDataArea-anchor', href=True)
        for address in addresses:
            locations.append(address.text.replace("\n", "").strip().replace(" |", ""))
        prices = clean_data(prices)
        prices = clean_data(prices)
        for link in links:
            hrefs.append(link['href'])
        for number in range(len(locations)):
            master = (locations[number], prices[number], hrefs[number])
            masters.append(master)
        return masters
    except Exception as e:
        print(e)


zillow = gspread.service_account(filename="zillow-researcher-212617f49fa2.json")
sh = zillow.open('Zillow Researcher').sheet1

masters = make_soup()
print(masters)
count = sh.row_count
sh.delete_rows(2, count)
for m in masters:
    sh.append_row(m)

