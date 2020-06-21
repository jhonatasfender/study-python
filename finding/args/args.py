import argparse


class Args:
    arguments = {
        '--database': 'Do the bar option',
        '--term': 'Foo the program',
        '--columns': 'Foo the program',
        '--file-in': 'Esse é o arquivo será lido',
        '--db-user': 'Usuário do banco de dado',
        '--db-pass': 'Senha do banco de dado',
        '--db': 'Nome da base de dados',
        '--name-table-of-term': """Nessa parte terá que ser colocado conforme o nome da tabela que será gravada
        de preferencia o nome do termo dá pesquisa""",
        '--only-one-url': 'Esse comando serve para quando quer processar somente uma url se a necessidade '
                          'de passar por um arquivo',
        '--only-one-name-for-search': 'Assim que o --only-one-url for preenchido deverá preencher também esse parâmetro'
                                      'para que possa ser pesquisado também junto com a url'
    }

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.add_arguments()

    def add_arguments(self):
        for key, val in self.arguments.items():
            self.parser.add_argument(key, help=val)

    def parse(self):
        return self.parser.parse_args()
