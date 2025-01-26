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
