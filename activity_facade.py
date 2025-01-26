# activity_facade.py

from singleton_db import SingletonDB
from observers import (
    ActivityAnalytics,
    QualitativeAnalyticsObserver,
    QuantitativeAnalyticsObserver,
)


class ActivityFacade:
    def __init__(self):
        self.db_service = SingletonDB()
        self.analytics = ActivityAnalytics(self.db_service)

        # Anexar observadores
        self.analytics.attach(QualitativeAnalyticsObserver(self.db_service))
        self.analytics.attach(QuantitativeAnalyticsObserver(self.db_service))

    def create_activity(self, activity_id: str):
        activity = self.db_service.create_activity(activity_id)
        self.analytics.notify(activity_id, "system", {"acesso_atividade": True})
        return activity

    def update_activity(
        self, activity_id: str, resumo: str = None, instrucoes: str = None
    ):
        updated_activity = self.db_service.update_activity(
            activity_id, resumo, instrucoes
        )
        self.analytics.notify(activity_id, "system", {"atividade_atualizada": True})
        return updated_activity

    def get_analytics_list(self):
        return {
            "qualAnalytics": [
                {"name": "Acesso à atividade", "type": "boolean"},
                {"name": "Download de recursos", "type": "boolean"},
            ],
            "quantAnalytics": [
                {"name": "Número de acessos", "type": "integer"},
                {"name": "Progresso na atividade", "type": "percentage"},
            ],
        }
