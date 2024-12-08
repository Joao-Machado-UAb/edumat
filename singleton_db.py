# singleton_db.py

DEFAULT_RESUMO = "Resumo de equações de 7º ano: Aqui você pode encontrar um resumo das equações de 7º ano."


class SingletonDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonDB, cls).__new__(cls)
            cls._instance.db = {}
        return cls._instance

    def get_instance(self):
        return self._instance.db

    def create_instance(self, activity_id):
        if activity_id not in self._instance.db:
            self._instance.db[activity_id] = {
                "resumo": DEFAULT_RESUMO,
                "instrucoes": "https://www.matematica.pt/aulas-matematica.php?ano=7",
            }
        return self._instance.db[activity_id]

    def access_data(self, activity_id):
        return self._instance.db.get(activity_id, None)

    def execute_operations(self, activity_id, resumo, instrucoes):
        if activity_id in self._instance.db:
            self._instance.db[activity_id]["resumo"] = resumo
            self._instance.db[activity_id]["instrucoes"] = instrucoes
        return self._instance.db[activity_id]
