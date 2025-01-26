# activity_facade.py

from singleton_db import Singleton_db
from observers import (
    AnalyticsService,
    QualitativeAnalyticsStrategy,
    QuantitativeAnalyticsStrategy,
)


class ActivityFacade:
    """Facade para gestão unica de atividades e analytics"""

    def __init__(self):
        self.db_service = Singleton_db()
        self.analytics_service = AnalyticsService(
            [QualitativeAnalyticsStrategy(), QuantitativeAnalyticsStrategy()]
        )

    def create_activity(self, activity_id: str):
        """Cria uma nova atividade"""
        activity = self.db_service.create_activity(activity_id)
        self.analytics_service.record_analytics(
            activity_id, "system", {"acesso_atividade": True}
        )
        return activity

    def update_activity(
        self, activity_id: str, resumo: str = None, instrucoes: str = None
    ):
        """Atualiza uma atividade existente"""
        updated_activity = self.db_service.update_activity(
            activity_id, resumo, instrucoes
        )
        self.analytics_service.record_analytics(
            activity_id, "system", {"atividade_atualizada": True}
        )
        return updated_activity

    def get_activity_analytics(self, activity_id: str):
        """Recupera analytics de uma atividade"""
        # Implementação de recuperação de analytics
        pass

    def get_analytics_list(self):
        """Lista de métricas de analytics disponíveis"""
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
