import requests
from lxml import html
from bs4 import BeautifulSoup
import csv
import pandas as pd

names = []
prices = []
changes = []
percentChanges = []
marketCaps = []
totalVolumes = []
circulatingSupplys = []
ttm = []

url = 'https://in.finance.yahoo.com/most-active'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "lxml")

for listing in soup.find_all('tr', attrs={'class': 'simpTblRow'}):
    for name in listing.find_all('td', attrs={'aria-label': 'Name'}):
        names.append(name.text)
    for price in listing.find_all('td', attrs={'aria-label': 'Price (intraday)'}):
        prices.append(price.find('span').text)
    for change in listing.find_all('td', attrs={'aria-label': 'Change'}):
        changes.append(change.text)
    for percentChange in listing.find_all('td', attrs={'aria-label': '% change'}):
        percentChanges.append(percentChange.text)
    for marketCap in listing.find_all('td', attrs={'aria-label': 'Market cap'}):
        marketCaps.append(marketCap.text)
    for totalVolume in listing.find_all('td', attrs={'aria-label': 'Avg vol (3-month)'}):
        totalVolumes.append(totalVolume.text)
    for circulatingSupply in listing.find_all('td', attrs={'aria-label': 'Volume'}):
        circulatingSupplys.append(circulatingSupply.text)
    # for ttm in listing.find_all('td', attrs={'aria-label': 'PE Ratio (TTM)'}):
    #     ttm.append(ttm.find('span').text)

df = pd.DataFrame(
    {"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Market Cap": marketCaps,"Average Volume": totalVolumes, "Volume": circulatingSupplys})
print(df.head())
df.to_json(r'Name.json')
