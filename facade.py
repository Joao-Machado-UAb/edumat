# facade.py
from singleton_db import SingletonDB


class ActivityFacade:
    def __init__(self):
        self._db = SingletonDB()
        self._analytics_data = {}

    def get_activity_config(self, activity_id):
        return {
            "params": [
                {"name": "resumo", "type": "text/plain"},
                {"name": "instrucoes", "type": "text/plain"},
            ]
        }

    def get_analytics_config(self):
        return {
            "qualAnalytics": [
                {"name": "Acesso à atividade", "type": "boolean"},
                {"name": "Download de recursos", "type": "boolean"},
                {"name": "Upload de documentos", "type": "boolean"},
                {"name": "Relatório das respostas", "type": "text/plain"},
            ],
            "quantAnalytics": [
                {"name": "Número de acessos", "type": "integer"},
                {"name": "Download de recursos", "type": "integer"},
                {"name": "Progresso na atividade (%)", "type": "integer"},
            ],
        }

    def deploy_activity(self, activity_id, student_id=None, params=None):
        self._db.create_instance(activity_id)
        if params:
            self._db.execute_operations(
                activity_id, params.get("resumo"), params.get("instrucoes")
            )

        base_url = "https://edumat.onrender.com/atividade"
        url = f"{base_url}?id={activity_id}"
        if student_id:
            url += f"&student_id={student_id}"
        return {"url": url}

    def get_activity_data(self, activity_id):
        data = self._db.access_data(activity_id)
        if not data:
            data = {
                "resumo": "Resumo de equações de 7º ano",
                "instrucoes": "https://www.matematica.pt/aulas-matematica.php?ano=7",
            }
        return data

    def get_analytics(self, activity_id=None, student_id=None):
        # Simulação de dados de analytics
        return [
            {
                "inveniraStdID": student_id or 1001,
                "qualAnalytics": [
                    {"name": "Acesso à atividade", "value": True},
                    {"name": "Download de recursos", "value": True},
                    {"name": "Upload de documentos", "value": True},
                    {"name": "Relatório das respostas", "value": "Suficiente"},
                ],
                "quantAnalytics": [
                    {"name": "Número de acessos", "value": 50},
                    {"name": "Download de recursos", "value": 12},
                    {"name": "Progresso na atividade (%)", "value": 10.0},
                ],
            }
        ]
