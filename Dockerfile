FROM python:3.6-stretch

RUN apt-get update && apt-get install -y mongodb git libleptonica-dev \
    tesseract-ocr tesseract-ocr-por libtesseract-dev

COPY finding-cpf.py finding-cpf.py
COPY files-imports /files-imports

RUN pip install --upgrade pip

RUN pip install PyPDF2 requests \
                bs4 fake_useragent \
                protobuf unidecode \
                openpyxl pdf2image \
                pymongo pytesseract pymongo[srv] \
                future selenium

RUN pip install git+https://github.com/abenassi/Google-Search-API               

RUN python finding-cpf.py

# CMD [ "python", "finding-cpf.py" ]