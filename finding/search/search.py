import os
import random
import re
import tempfile
import time
import traceback
from urllib.parse import urlencode

import PyPDF2
import requests
from PyPDF2.utils import PdfReadError
from bs4 import BeautifulSoup
from google import google
from openpyxl import load_workbook
from pdf2image import convert_from_path
from pytesseract import image_to_string
from urllib3.exceptions import InsecureRequestWarning

from finding.search.connection import Connection


class Search:
    __count = 0
    __configuration = None
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

    def __init__(self, args):
        self.args = args
        self.clear_console()
        self.connection = Connection(args)
        self.__get_csv()
        self.assign_current_reading_value_file()

        self.read()

    def processing_google_result(self, result, i, name, values, lawyer):
        link = result.link
        print(i + 1, name, link)

        if self.connection.table().find({"link": link}).count() == 0:
            response = None
            html_text = None
            try:
                response = requests.get(result.link, headers=self.__headers)
            except ConnectionError as e:
                self.log(i, name, link)
                return
            except requests.exceptions.SSLError as e:
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                response = requests.get(result.link, verify=False, headers=self.__headers)

            if response.status_code == 404:
                return

            if response.headers._store['content-type'][1].count('pdf'):
                html_text = self.read_pdf(response)
            else:
                html = BeautifulSoup(response.text, "html.parser")
                html_text = html.text
                pass

            if html_text.count(name):
                find_phone = re.findall(r"(\(\d{2}\)\s?\d{4,5}-?\d{4})", html_text)
                find_cpf = re.findall(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", html_text)

                if len(find_phone) or len(find_cpf):
                    list_cpfs = []
                    for values_cpfs in find_cpf:
                        list_cpfs.append({
                            "cpf": values_cpfs,
                            "name": ""
                        })

                    self.connection.table().insert_one({
                        "name": name,
                        "phone": find_phone,
                        "cpf": list_cpfs,
                        "link": link,
                        "values": values,
                        "lawyer": lawyer
                    })
                    print(i + 1, name, link, str(find_phone), str(find_cpf))
                    pass
            pass

        self.__count = i + 1

    def __row(self, i):
        if i != 0 and i >= self.__count - 1:
            name = self.sheet.cell(row=i + 1, column=4).value.strip()
            lawyer = self.sheet.cell(row=i + 1, column=8).value.strip()
            values = self.sheet.cell(row=i + 1, column=12).value

            self.connection.get_configuration() \
                .update_one({"_id": self.__configuration.get('_id')}, {"$set": {"rowFromCSV": self.__count}})

            search_results = google.search('"' + lawyer + '" AND "' + name + '"', 1)

            for result in search_results:
                try:
                    self.processing_google_result(result, i, name, values, lawyer)
                except Exception:
                    self.log(i, name, result.link)
                    break

            time.sleep(random.randint(1, 30))

    def read(self):
        for i in range(self.row_count):
            self.__row(i)

    def assign_current_reading_value_file(self):
        self.__configuration = self.connection.get_configuration().find_one()
        self.__count = self.__configuration.get('rowFromCSV')

    def __get_csv(self):
        if self.args.file_in:
            self.workbook = load_workbook(self.args.file_in)
            self.sheet = self.workbook.active
            self.row_count = self.sheet.max_row
        else:
            raise ValueError('É obrigatório preencher o --file-in')

    @staticmethod
    def clear_console():
        os.system('clear')

    @staticmethod
    def telegram_bot_send_text(bot_message):
        bot_token = '700094640:AAEKqh3z7e6LfiXTXeFTpRnugSioqMkVA7o'
        bot_chat_id = ('1048049017', '680337670')
        for chat_id in bot_chat_id:
            query = {
                "chat_id": chat_id,
                "parse_mode": "markdown",
                "text": bot_message
            }
            send_text = "https://api.telegram.org/bot{token}/sendMessage?{query}" \
                .format(token=bot_token, query=urlencode(query))
            response = requests.get(send_text)
            print(response.json())

    @staticmethod
    def telegram_bot_delete_conversation():
        chat = requests.get("https://api.telegram.org/bot700094640:AAEKqh3z7e6LfiXTXeFTpRnugSioqMkVA7o/getUpdates")
        result_chat = chat.json()
        for conversation in result_chat.get('result'):
            message_id = conversation.get('message').get('message_id')
            chat_id = conversation.get('message').get('reply_to_message').get('chat').get('id')
            is_bot = conversation.get('message').get('reply_to_message').get('chat').get('is_bot')
            if is_bot:
                response_delete = requests.get(
                    "https://api.telegram.org/bot700094640:AAEKqh3z7e6LfiXTXeFTpRnugSioqMkVA7o/deleteMessage" +
                    "?chat_id=" + str(chat_id) + "&message_id=" + str(message_id)
                )
                print(response_delete.json())

    def log(self, i=None, name=None, link=None):
        if i or name or link:
            self.telegram_bot_send_text(
                str(i + 1) + "\n" +
                "*" + name + "*\n" +
                "[link](" + link + ")\n" +
                "```log" + traceback.format_exc() + "```"
            )
            print(str([i + 1, name, link]))
        else:
            self.telegram_bot_send_text("```log" + traceback.format_exc() + "```")

        print(traceback.format_exc())

    def read_pdf(self, response):
        text = ""
        try:
            name_and_directory_file = "/tmp/" + str(random.getrandbits(128)) + ".pdf"
            with open(name_and_directory_file, 'wb') as f:
                f.write(response.content)
                f.close()

            pdf = open(name_and_directory_file, "rb")
            read_pdf_extractor = PyPDF2.PdfFileReader(pdf, strict=False)
            max_pages_pdf = read_pdf_extractor.getNumPages()
            count_pages = 0
            while count_pages < max_pages_pdf:
                text += read_pdf_extractor.getPage(count_pages).extractText()
                count_pages += 1

            pdf.close()
            del pdf
            del read_pdf_extractor

            with tempfile.TemporaryDirectory() as path:
                for page in range(1, max_pages_pdf, 10):
                    images_from_path = convert_from_path(
                        name_and_directory_file, dpi=200, first_page=page,
                        last_page=min(page + 10 - 1, max_pages_pdf), output_folder=path
                    )

                    for img in images_from_path:
                        text += image_to_string(img, lang='por')

                    del images_from_path
            os.remove(name_and_directory_file)
        except PdfReadError:
            self.log()

        return text
