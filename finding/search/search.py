import os

from openpyxl import load_workbook

from finding.search.connection import Connection
from finding.search.processing_search import ProcessingSearch


class Search:
    __configuration = None

    def __init__(self, args):
        self.args = args
        self.clear_console()
        self.connection = Connection(args)
        self.__get_csv()
        self.assign_current_reading_value_file()

        self.read()

    def read(self):
        for i in range(self.row_count):
            ProcessingSearch.start(
                self.connection, i, self.sheet, self.__configuration,
                self.__configuration.get('rowFromCSV')
            )

    def assign_current_reading_value_file(self):
        self.__configuration = self.connection.get_configuration().find_one()

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
