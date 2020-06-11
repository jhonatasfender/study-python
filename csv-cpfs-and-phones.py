import csv
import os

from pymongo import MongoClient


class CSVWriter():
    filename = None
    fp = None
    writer = None

    def __init__(self, filename):
        self.filename = filename
        self.fp = open(self.filename, 'w', encoding='utf8')
        self.writer = csv.writer(self.fp, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

    def close(self):
        self.fp.close()

    def write(self, elems):
        self.writer.writerow(elems)

    def size(self):
        return os.path.getsize(self.filename)

    def fname(self):
        return self.filename


client = MongoClient('localhost', 27017)
db = client.miningNames
tablesNames = db.names
tablesUsers = db.users

mycsv = CSVWriter('name-phones.csv')

with open('name-cpf.csv', 'wb') as csvfile:
    for user in list(tablesNames.find({})):
        name = user.get('name')
        cpfs = user.get('cpf')
        phones = user.get('phone')

        # for cpf in cpfs:
        #     print(name, cpf.get('cpf'))
        #     mycsv.write((name, cpf.get('cpf')))

        for phone in phones:
            print((name, phone))
            mycsv.write((name, phone))


mycsv.close()
