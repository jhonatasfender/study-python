FROM python:3.6-stretch

RUN apt-get update && apt-get install -y mongodb

COPY finding-cpf.py finding-cpf.py
COPY files-imports /files-imports

RUN pip install --upgrade pip

RUN pip install PyPDF2 requests \
                bs4 fake_useragent \
                protobuf google-search \
                openpyxl pdf2image \
                pymongo pytesseract

RUN python finding-cpf.py

# CMD [ "python", "finding-cpf.py" ]