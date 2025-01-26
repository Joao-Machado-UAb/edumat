# observers.py

#  importação do módulo abc (Abstract Base Classes) do Python, que fornece infraestrutura para criar classes abstratas
from abc import ABC, abstractmethod

# importação do módulo typing (tipos genéricos do módulo typing):
# List - representa uma lista e permite especificar o tipo dos elementos contidos na lista;
# dict - permite especificar os tipos das chaves e valores do dicionário;
# Any - (int, str, list, etc.)
from typing import List, Dict, Any
from datetime import datetime
from singleton_db import DatabaseService
import json
import os



class AnalyticsObserver(ABC):
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    @abstractmethod
    def process(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        pass

class QualitativeAnalyticsObserver(AnalyticsObserver):
    def process(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        qualitative_data = {
            "student_id": student_id,
            "acesso_atividade": data.get("acesso_atividade", False),
            "download_recursos": data.get("download_recursos", False)
        }
        self.db_service.record_analytics(activity_id, "qualitative", qualitative_data)

class QuantitativeAnalyticsObserver(AnalyticsObserver):
    def process(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        quantitative_data = {
            "student_id": student_id,
            "numero_acessos": data.get("numero_acessos", 0),
            "progresso_atividade": data.get("progresso_atividade", 0.0)
        }
        self.db_service.record_analytics(activity_id, "quantitative", quantitative_data)

class ActivityAnalytics:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        self.observers = []

    def attach(self, observer: AnalyticsObserver):
        self.observers.append(observer)

    def notify(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        for observer in self.observers:
            observer.process(activity_id, student_id, data)
