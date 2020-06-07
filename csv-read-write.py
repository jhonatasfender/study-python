import csv
import PyPDF2
from tika import parser
c
import re

clear = lambda: os.system('clear')
clear()

os.remove("eggs.csv")

file = open("eggs.csv", "w+")
file.close()


raw = parser.from_file("/home/joantas/Downloads/read.pdf")

# read
with open('eggs.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print(', '.join(row))

# append
with open('eggs.csv', 'a') as csvfile:
    spamwriter = csv.writer(csvfile,
                            delimiter=',',
                            quotechar='|',
                            quoting=csv.QUOTE_MINIMAL)

    names = re.findall("(Precatório|Requerente|Advogado|Requerido|Deprecante)\s:(.*)", raw['content'])

    arr = []
    for key, name in enumerate(names):
        if name[0] == 'Precatório':
            spamwriter.writerow(arr)
            arr = []
            pass

        modifyName = name[1].strip().replace(' E OUTRO(A)', '')
        arr.append(modifyName)


