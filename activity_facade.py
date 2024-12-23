# activity_facade.py

from singleton_db import SingletonDB


class ActivityFacade:
    def __init__(self):
        self.db = SingletonDB()

    def create_activity(self, activity_id):
        """
        Cria ou retorna uma atividade existente no banco de dados.
        """
        return self.db.create_instance(activity_id)

    def get_activity_data(self, activity_id):
        """
        Retorna os dados da atividade.
        """
        return self.db.access_data(activity_id)

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        """
        Atualiza os dados de uma atividade.
        """
        return self.db.execute_operations(activity_id, resumo, instrucoes)
