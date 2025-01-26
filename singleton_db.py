# singleton_db.py (refatorado)

DEFAULT_RESUMO = "Resumo de equações de 7º ano: Aqui pode encontrar um resumo de equações de 7º ano."

class SingletonDB:
    """
    Classe Singleton que gerencia a instância única do banco de dados.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonDB, cls).__new__(cls)
            cls._instance.db = {}
        return cls._instance

    def get_database(self):
        return self._instance.db


class ActivityRepository:
    """
    Classe responsável por gerenciar operações relacionadas às atividades no banco de dados.
    """
    def __init__(self, db_instance):
        self.db = db_instance

    def create_activity(self, activity_id):
        """
        Cria uma entrada no banco de dados se ela não existir.

        Parâmetros:
            activity_id (str): ID da atividade a ser criada.

        Retorna:
            dict: A entrada criada ou já existente.
        """
        if activity_id not in self.db:
            self.db[activity_id] = {
                "resumo": DEFAULT_RESUMO,
                "instrucoes": "https://www.matematica.pt/aulas-matematica.php?ano=7",
            }
        return self.db[activity_id]

    def get_activity(self, activity_id):
        """
        Retorna os dados de uma entrada específica.

        Parâmetros:
            activity_id (str): ID da atividade a ser acessada.

        Retorna:
            dict ou None: Os dados da entrada, ou None se não existir.
        """
        return self.db.get(activity_id, None)

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        """
        Atualiza os dados de uma entrada existente no banco de dados.

        Parâmetros:
            activity_id (str): ID da atividade a ser atualizada.
            resumo (str, opcional): Novo resumo.
            instrucoes (str, opcional): Novas instruções.

        Retorna:
            dict: Os dados atualizados da entrada.

        Lança:
            KeyError: Se o ID da atividade não for encontrado no banco de dados.
        """
        if activity_id not in self.db:
            raise KeyError(f"Activity ID '{activity_id}' não encontrado no banco de dados.")
        if resumo:
            self.db[activity_id]["resumo"] = resumo
        if instrucoes:
            self.db[activity_id]["instrucoes"] = instrucoes
        return self.db[activity_id]

