import os
import random
import tempfile

import PyPDF2
from PyPDF2.utils import PdfReadError
from pdf2image import convert_from_path
from pytesseract import image_to_string

from finding.search.logger import Logger


class ReadPDF:
    __text = ""

    @staticmethod
    def start(response):
        r = ReadPDF()
        r.__read(response)

    def __read(self, response):
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
                self.__text += read_pdf_extractor.getPage(count_pages).extractText()
                count_pages += 1

            pdf.close()
            del pdf
            del read_pdf_extractor

            with tempfile.TemporaryDirectory() as path:
                for page in range(1, max_pages_pdf, 100):
                    images_from_path = convert_from_path(
                        name_and_directory_file, dpi=200, first_page=page,
                        last_page=min(page + 100 - 1, max_pages_pdf), output_folder=path
                    )

                    for img in images_from_path:
                        self.__text += image_to_string(img, lang='por')

                    del images_from_path
            os.remove(name_and_directory_file)
        except PdfReadError:
            Logger.log()

        return self.__text
