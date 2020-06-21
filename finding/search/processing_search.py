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
    def start_with_csv(connection, i, sheet, configuration, count):
        start = ProcessingSearch(
            connection=connection,
            sheet=sheet,
            configuration=configuration,
            count=count
        )
        start.row(i)

    @staticmethod
    def start_single_name(connection, configuration, name, term):
        start = ProcessingSearch(
            connection=connection,
            configuration=configuration
        )
        start.search_single_name(name, term)

    def __init__(self, connection, configuration, sheet=None, count=None):
        self.connection = connection
        self.sheet = sheet
        self.__configuration = configuration
        self.__count = count

    def search_single_name(self, name, term):

        search_results = google.search('"' + name + '" AND "' + term + '"', 1)

        for result in search_results:
            find_phone = []
            find_cpf = []
            find_cnpj = []
            try:
                link = result.link
                html_text = self.response_link(result=result, name=name)

                for m in re.finditer(name.upper(), html_text.upper()):
                    [start, end] = m.span()

                    html = html_text[start - 200:end + 200]

                    find_phone = find_phone + re.findall(r"(\(\d{2}\)\s?\d{4,5}-?\d{4})", html)
                    find_cpf = find_cpf + re.findall(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", html)
                    find_cnpj = find_cnpj + re.findall(r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}", html)

                valid_if_exists_url = self.connection.table().find({"link": link}).count() == 0
                if valid_if_exists_url and (len(find_phone) or len(find_cpf)):
                    find_phone = list(dict.fromkeys(find_phone))
                    find_cpf = list(dict.fromkeys(find_cpf))
                    find_cnpj = list(dict.fromkeys(find_cnpj))
                    self.save_table_phone_and_cpf_cpnj(name, find_phone, find_cpf, find_cnpj, link)
                    print(name, str(find_phone), str(find_cpf), str(find_cnpj))
            except Exception:
                Logger.log(name=name, link=result.link)
                break

        time.sleep(random.randint(1, 30))

    def response_link(self, result, i=None, name=None, link=None):
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

        return re.sub(r"\n", r"", html_text)

    def save_table(self, name, find_phone, list_cpfs, link, values, lawyer):
        self.connection.table().insert_one({
            "name": name,
            "phone": find_phone,
            "cpf": list_cpfs,
            "link": link,
            "values": values,
            "lawyer": lawyer
        })

    def save_table_phone_and_cpf(self, name, find_phone, list_cpfs, link):
        self.connection.table().insert_one({
            "name": name,
            "phone": find_phone,
            "cpf": list_cpfs,
            "link": link,
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
        html_text = self.response_link(result, i, name, link)

        if html_text.count(name):
            find_phone = re.findall(r"(\(\d{2}\)\s?\d{4,5}-?\d{4})", html_text)
            find_cpf = re.findall(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", html_text)

            if len(find_phone) or len(find_cpf):
                list_cpfs = []
                for values_cpfs in find_cpf:
                    self.save_cpf(list_cpfs, values_cpfs)
                self.save_table(name, find_phone, list_cpfs, link, values, lawyer)
                print(i + 1, name, link, str(find_phone), str(find_cpf))

    def __processing_google_result(self, result, name, i=None, values=None, lawyer=None):
        link = result.link
        if i:
            print(i + 1, name, link)

        if self.connection.table().find({"link": link}).count() == 0:
            self.after_validating_that_link_already_exists(
                result, i, name, link, values, lawyer
            )

        if i:
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

    def save_table_phone_and_cpf_cpnj(self, name, find_phone, find_cpf, find_cnpj, link):
        self.connection.table().insert_one({
            "name": name,
            "phone": find_phone,
            "cpf": find_cpf,
            "cnpj": find_cnpj,
            "link": link,
        })
