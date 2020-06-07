
import requests
import re
from bs4 import BeautifulSoup
import os

clear = lambda: os.system('clear')
clear()

response = requests.get('https://edj.trf1.jus.br/edj/bitstream/handle/123/14313/Caderno_JUD_GO_2018-09-12_X_170.pdf?sequence=1&isAllowed=y')

html = BeautifulSoup(response.text, "html.parser")

name = 'MERCIA VAZ LOPES'

# p = re.compile(html.text)
# findName = re.match(name,html.text)

findName = html.text.count(name)

if findName:

    findPhone = re.findall(r"(\(\d{2}\)\s?\d{4,5}\-?\d{4})",
                            html.text)
    findCPF = re.findall(r"(\d{3}\.\d{3}\.\d{3}\-\d{2})",
                            html.text)

    # for phone in findPhone:
    #     spamwriter.writerow([name, phone, link.link])
    if len(findPhone) or len(findCPF):
        print(name, findPhone, findCPF)

        pass
pass