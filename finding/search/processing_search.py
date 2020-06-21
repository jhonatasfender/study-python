import random
import re
import time

import requests
from bs4 import BeautifulSoup
from google import google
from urllib3.exceptions import InsecureRequestWarning

from finding.search.logger import Logger
from finding.search.read_pdf import ReadPDF


class ProcessingSearch:
    __count = 0
    __headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'connection': 'keep-alive',
    }

    @staticmethod
    def start(connection, i, sheet, configuration, count):
        start = ProcessingSearch(connection, sheet, configuration, count)
        start.row(i)

    def __init__(self, connection, sheet, configuration, count):
        self.connection = connection
        self.sheet = sheet
        self.__configuration = configuration
        self.__count = count

    def respose_link(self, result, i, name, link):
        html_text = None
        try:
            response = requests.get(result.link, headers=self.__headers)
        except ConnectionError as e:
            Logger.log(i, name, link)
            return
        except requests.exceptions.SSLError as e:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(result.link, verify=False, headers=self.__headers)

        if response.status_code == 404:
            return

        if response.headers._store['content-type'][1].count('pdf'):
            html_text = ReadPDF.start(response)
        else:
            html_text = BeautifulSoup(response.text, "html.parser").text

        return html_text

    def save_table(self, name, find_phone, list_cpfs, link, values, lawyer):
        self.connection.table().insert_one({
            "name": name,
            "phone": find_phone,
            "cpf": list_cpfs,
            "link": link,
            "values": values,
            "lawyer": lawyer
        })

    @staticmethod
    def save_cpf(list_cpfs, values_cpfs):
        list_cpfs.append({
            "cpf": values_cpfs,
            "name": ""
        })

    def after_validating_that_link_already_exists(
            self, result, i, name, link, values, lawyer
    ):
        html_text = self.respose_link(result, i, name, link)

        if html_text and html_text.count(name) and lawyer and html_text.count(lawyer):
            find_phone = re.findall(r"(\(\d{2}\)\s?\d{4,5}-?\d{4})", html_text)
            find_cpf = re.findall(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", html_text)

            if len(find_phone) or len(find_cpf):
                list_cpfs = []
                for values_cpfs in find_cpf:
                    self.save_cpf(list_cpfs, values_cpfs)
                self.save_table(name, find_phone, list_cpfs, link, values, lawyer)
                print(i + 1, name, link, str(find_phone), str(find_cpf))

    def __processing_google_result(self, result, i, name, values, lawyer):
        link = result.link
        print(i + 1, name, link)

        if self.connection.table().find({"link": link}).count() == 0:
            self.after_validating_that_link_already_exists(
                result, i, name, link, values, lawyer
            )
        self.__count = i + 1

    def row(self, i):
        if i != 0 and i >= self.__count - 1:
            name = self.sheet.cell(row=i + 1, column=4).value
            lawyer = self.sheet.cell(row=i + 1, column=8).value
            values = self.sheet.cell(row=i + 1, column=12).value

            self.connection.get_configuration() \
                .update_one({"_id": self.__configuration.get('_id')}, {"$set": {"rowFromCSV": self.__count}})

            if not lawyer or not values:
                return

            search_results = google.search('"' + lawyer.strip() + '" AND "' + name.strip() + '"', 1)

            for result in search_results:
                try:
                    self.__processing_google_result(result, i, name, values, lawyer)
                except Exception:
                    Logger.log(i, name, result.link)
                    break

            time.sleep(random.randint(1, 30))
