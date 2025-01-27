# activity_manager.py (refatorização)

from typing import Dict, Any, Optional
from datetime import datetime
from observers import ActivityAnalytics, QualitativeAnalyticsObserver, QuantitativeAnalyticsObserver

class ActivityManager:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ActivityManager, cls).__new__(cls)
            cls._instance.activities = {}
            cls._instance.analytics = ActivityAnalytics()
            # Inicializar analytics observers
            cls._instance.analytics.attach(QualitativeAnalyticsObserver())
            cls._instance.analytics.attach(QuantitativeAnalyticsObserver())
        return cls._instance

    def create_activity(self, activity_id: str) -> Dict[str, Any]:
        if activity_id not in self.activities:
            self.activities[activity_id] = {
                "resumo": "Resumo de equações de 7º ano: Aqui pode encontrar um resumo de equações de 7º ano.",
                "instrucoes": "https://www.matematica.pt/aulas-matematica.php?ano=7",
                "created_at": datetime.now().isoformat(),
                "access_count": 0
            }
        return self.activities[activity_id]

    def get_activity(self, activity_id: str, student_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        activity = self.activities.get(activity_id)
        if activity and student_id:
            self.activities[activity_id]["access_count"] += 1
            self.record_activity_access(activity_id, student_id)
        return activity

    def update_activity(self, activity_id: str, resumo: Optional[str] = None, 
                       instrucoes: Optional[str] = None) -> Dict[str, Any]:
        if activity_id not in self.activities:
            raise KeyError(f"Atividade '{activity_id}' não encontrada.")
            
        if resumo:
            self.activities[activity_id]["resumo"] = resumo
        if instrucoes:
            self.activities[activity_id]["instrucoes"] = instrucoes
            
        self.activities[activity_id]["updated_at"] = datetime.now().isoformat()
        return self.activities[activity_id]

    def record_activity_access(self, activity_id: str, student_id: str):
        self.analytics.record_activity(
            activity_id,
            student_id,
            {
                "acesso_atividade": True,
                "numero_acessos": self.activities[activity_id]["access_count"]
            }
        )

    def get_analytics_list(self) -> Dict[str, list]:
        return {
            "qualAnalytics": [
                {"name": "Acesso à atividade", "type": "boolean"},
                {"name": "Download de recursos", "type": "boolean"},
                {"name": "Upload de documentos", "type": "boolean"},
                {"name": "Relatório das respostas concretamente dadas", "type": "text/plain"},
            ],
            "quantAnalytics": [
                {"name": "Número de acessos", "type": "integer"},
                {"name": "Download de recursos", "type": "integer"},
                {"name": "Progresso na atividade (%)", "type": "integer"},
            ],
        }
