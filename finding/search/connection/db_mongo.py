import os

from pymongo import MongoClient


class Connection:
    __client = None
    __db = None

    def __init__(self, args):
        self.args = args
        self.__validation()
        self.mongo_client()
        self.__select_db_name()

    def mongo_client(self):
        self.__client = MongoClient(self.connection_url().format(
            user=self.user, password=self.password, db=self.db_name
        ))

    def __set_environment(self):
        self.user = os.getenv('URL_CONNECTION_MONGODB_MINING_NAME_USER')
        self.password = os.getenv('URL_CONNECTION_MONGODB_MINING_NAME_PASS')
        self.db_name = os.getenv('URL_CONNECTION_MONGODB_MINING_NAME_DB')

    def __exc_is_not_auth(self):
        raise ValueError("""
            Por favor adicione as variáveis de ambiente:
            export URL_CONNECTION_MONGODB_MINING_NAME_USER=********
            export URL_CONNECTION_MONGODB_MINING_NAME_PASS=********
            export URL_CONNECTION_MONGODB_MINING_NAME_DB=********

            Ou adicionar os parâmetros
            --db-user ***********
            --db-pass ************
            --db *********
        """)

    def __validation(self):
        self.__set_environment()
        if not self.user or not self.password or not self.db_name:
            if not self.args.db_user or not self.args.db_pass or not self.args.db:
                self.__exc_is_not_auth()
            else:
                self.user = self.args.db_user
                self.password = self.args.db_pass
                self.db_name = self.args.db

    def __select_db_name(self):
        self.__db = self.__client.get_database('mining-name')

    def table(self):
        if self.args.name_table_of_term:
            return self.__db.get_collection(self.args.name_table_of_term)
        else:
            raise ValueError('É obrigatório que preencha o --name-table-of-term')

    def get_configuration(self):
        return self.__db.get_collection('configuration')

    @staticmethod
    def connection_url() -> str:
        return "mongodb+srv://{user}:{password}@intelligent-mind-information-pnrix.mongodb.net/{db}?retryWrites=true&w=majority"
