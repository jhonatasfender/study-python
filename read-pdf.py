import io
import os
import random
import tempfile

import PyPDF2
import requests
from pdf2image import pdf2image, convert_from_path

# url = 'http://localhost:8000/test.pdf'
from pytesseract import image_to_string

url = "http://www.copese.uft.edu.br/resultado_vestibular_2012_02_UFT.pdf"
response = requests.get(url)

text = ""

hash_for_name_file = random.getrandbits(128)
name_and_directory_file = "/tmp/" + str(random.getrandbits(128)) + ".pdf"

with open(name_and_directory_file, 'wb') as f:
    f.write(response.content)
    f.close()

pdf = open(name_and_directory_file, "rb")
read_pdf = PyPDF2.PdfFileReader(pdf)
maxPages = read_pdf.getNumPages()
count = 0
while count < maxPages:
    text += read_pdf.getPage(count).extractText()
    count += 1

pdf.close()
del pdf
del read_pdf

with tempfile.TemporaryDirectory() as path:
    for page in range(1, maxPages, 10):
        images_from_path = convert_from_path(
            name_and_directory_file, dpi=200, first_page=page,
            last_page=min(page + 10 - 1, maxPages), output_folder=path
        )

        for img in images_from_path:
            text += image_to_string(img, lang='por')

del images_from_path

os.remove(name_and_directory_file)

print(text)
