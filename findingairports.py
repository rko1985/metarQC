import requests
from bs4 import BeautifulSoup
import re

URL = "https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States"
r = requests.get(URL) 

soup = BeautifulSoup(r.content, 'html5lib') 
tds = soup.findAll('td')

airports = []

for td in tds:
    airport = re.findall(r"[A-Z]{4}", td.text)
    if len(airport) > 0:
        airports.append(airport[0])

print(airports)
   
