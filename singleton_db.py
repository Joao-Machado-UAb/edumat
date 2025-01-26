# observers.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from singleton_db import SingletonDB


class AnalyticsObserver(ABC):
    def __init__(self, db_service: SingletonDB):
        self.db_service = db_service

    @abstractmethod
    def process(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        pass


class QualitativeAnalyticsObserver(AnalyticsObserver):
    def process(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        qualitative_data = {
            "student_id": student_id,
            "acesso_atividade": data.get("acesso_atividade", False),
            "download_recursos": data.get("download_recursos", False),
        }
        self.db_service.record_analytics(activity_id, "qualitative", qualitative_data)


class QuantitativeAnalyticsObserver(AnalyticsObserver):
    def process(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        quantitative_data = {
            "student_id": student_id,
            "numero_acessos": data.get("numero_acessos", 0),
            "progresso_atividade": data.get("progresso_atividade", 0.0),
        }
        self.db_service.record_analytics(activity_id, "quantitative", quantitative_data)


class ActivityAnalytics:
    def __init__(self, db_service: SingletonDB):
        self.db_service = db_service
        self.observers = []

    def attach(self, observer: AnalyticsObserver):
        self.observers.append(observer)

    def notify(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        for observer in self.observers:
            observer.process(activity_id, student_id, data)
