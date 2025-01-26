# observer.py

#  importação do módulo abc (Abstract Base Classes) do Python, que fornece infraestrutura para criar classes abstratas
from abc import ABC, abstractmethod

# importação do módulo typing (tipos genéricos do módulo typing):
# List - representa uma lista e permite especificar o tipo dos elementos contidos na lista;
# dict - permite especificar os tipos das chaves e valores do dicionário;
# Any - (int, str, list, etc.)
from typing import List, Dict, Any
from datetime import datetime
import json
import os

class AnalyticsStrategy(ABC):
    """Estratégia abstrata para processamento de analytics"""

    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class QualitativeAnalyticsStrategy(AnalyticsStrategy):
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "qualitative",
            "acesso_atividade": data.get("acesso_atividade", False),
            "download_recursos": data.get("download_recursos", False),
            "upload_documentos": data.get("upload_documentos", False),
        }


class QuantitativeAnalyticsStrategy(AnalyticsStrategy):
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "quantitative",
            "numero_acessos": data.get("numero_acessos", 0),
            "progresso_atividade": data.get("progresso_atividade", 0.0),
        }


class AnalyticsService:
    """Serviço centralizado de processamento de analytics"""

    def __init__(self, strategies: list):
        self.strategies = strategies
        self._ensure_analytics_dir()

    def _ensure_analytics_dir(self):
        os.makedirs("analytics_data", exist_ok=True)

    def record_analytics(self, activity_id: str, student_id: str, data: Dict[str, Any]):
        """Processa e grava dados de analytics"""
        processed_data = {
            "activity_id": activity_id,
            "student_id": student_id,
            "timestamp": datetime.now().isoformat(),
        }

        for strategy in self.strategies:
            processed_data.update(strategy.process(data))

        self._save_to_file(processed_data, activity_id)

    def _save_to_file(self, data: Dict[str, Any], activity_id: str):
        """Grava dados de analytics em ficheiro JSON"""
        filename = f"analytics_data/{data['type']}_{activity_id}.json"

        existing_data = self._load_existing_data(filename)
        existing_data.append(data)

        with open(filename, "w") as file:
            json.dump(existing_data, file, indent=4)

    def _load_existing_data(self, filename: str) -> list:
        """Carrega dados existentes ou retorna lista vazia"""
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

