import csv

import requests
from bs4 import BeautifulSoup

url = 'https://portal.trf1.jus.br/data/files/62/62/D4/A3/B1C4271069F4A427E52809C2/precatorios%20federais%202020%20-%20Resolu__o%20303%20do%20CNJ.htm'
f = requests.get(url)
soup = BeautifulSoup(f.text, "html.parser")
table = soup.select_one("table")
# python3 just use th.text
headers = [th.text for th in table.select("tr th")]


def remover(text):
    format_text = text.translate(str.maketrans('', '', '\n\t\r'))
    return format_text


with open("out.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(headers)
    wr.writerows([[remover(td.text) for td in row.find_all("td")] for row in table.select("tr + tr")])
