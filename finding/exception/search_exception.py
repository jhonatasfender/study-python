class SearchException:

    @staticmethod
    def choose_a_file_mining_type_or_simple_name():
        raise ValueError("""
            É necessário que selecione uma dessas opções:

                --name-table-of-term "name-of-the-applicant-and-the-lawyer"
                --file-in ../files-imports/lista-control-precatorio-14-10-2019-gpi.xlsx

            Ou

                --name-term
                --name-search
        """)
