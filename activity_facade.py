# activity_facade.py (refatorado)

from singleton_db import SingletonDB, ActivityRepository
from observers import (
    ActivityAnalytics,
    QualitativeAnalyticsObserver,
    QuantitativeAnalyticsObserver,
)

class ActivityFacade:
    def __init__(self):
        # Inicializar o banco de dados e repositório
        self.db = SingletonDB().get_database()
        self.repository = ActivityRepository(self.db)

        # Inicializar o sistema de analytics
        self.analytics = ActivityAnalytics()

        # Anexar os observers
        self.analytics.attach(QualitativeAnalyticsObserver())
        self.analytics.attach(QuantitativeAnalyticsObserver())

    def create_activity(self, activity_id):
        """
        Cria uma nova atividade no banco de dados usando o repositório.

        Parâmetros:
            activity_id (str): ID da atividade a ser criada.

        Retorna:
            dict: Dados da atividade criada.
        """
        return self.repository.create_activity(activity_id)

    def access_activity_data(self, activity_id):
        """
        Registra o acesso à atividade e retorna os seus dados.

        Parâmetros:
            activity_id (str): ID da atividade a ser acedida.

        Retorna:
            dict ou None: Dados da atividade.
        """
        if activity_id:
            self.analytics.record_activity(
                activity_id,
                "student_test",  # Passar aqui o ID do estudante
                {"acesso_atividade": True, "numero_acessos": 1},
            )
        return self.repository.get_activity(activity_id)

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        """
        Atualiza os dados duma atividade existente.

        Parâmetros:
            activity_id (str): ID da atividade a ser atualizada.
            resumo (str, opcional): Novo resumo.
            instrucoes (str, opcional): Novas instruções.

        Retorna:
            dict: Dados atualizados da atividade.
        """
        return self.repository.update_activity(activity_id, resumo, instrucoes)

    def get_analytics_list(self):
        """
        Retorna a lista de tipos de analytics disponíveis.

        Retorna:
            dict: Dados de analytics qualitativos e quantitativos.
        """
        return {
            "qualAnalytics": [
                {"name": "Acesso à atividade", "type": "boolean"},
                {"name": "Download de recursos", "type": "boolean"},
                {"name": "Upload de documentos", "type": "boolean"},
                {
                    "name": "Relatório das respostas concretamente dadas",
                    "type": "text/plain",
                },
            ],
            "quantAnalytics": [
                {"name": "Número de acessos", "type": "integer"},
                {"name": "Download de recursos", "type": "integer"},
                {"name": "Progresso na atividade (%)", "type": "integer"},
            ],
        }

    def get_analytics_data(self):
        """
        Retorna os dados de analytics registrados.

        Retorna:
            list: Lista de dados de analytics por estudante.
        """
        return [
            {
                "inveniraStdID": 1001,
                "qualAnalytics": [
                    {"name": "Acesso à atividade", "value": True},
                    {"name": "Download de recursos", "value": True},
                    {"name": "Upload de documentos", "value": True},
                    {
                        "name": "Relatório das respostas concretamente dadas",
                        "value": "Suficiente",
                    },
                ],
                "quantAnalytics": [
                    {"name": "Número de acessos", "value": 50},
                    {"name": "Download de recursos", "value": 12},
                    {"name": "Progresso na atividade (%)", "value": 10.0},
                ],
            },
            {
                "inveniraStdID": 1002,
                "qualAnalytics": [
                    {"name": "Acesso à atividade", "value": True},
                    {"name": "Download de recursos", "value": True},
                    {"name": "Upload de documentos", "value": True},
                    {
                        "name": "Relatório das respostas concretamente dadas",
                        "value": "Suficiente",
                    },
                ],
                "quantAnalytics": [
                    {"name": "Número de acessos", "value": 60},
                    {"name": "Download de recursos", "value": 16},
                    {"name": "Progresso na atividade (%)", "value": 40.0},
                ],
            },
        ]
