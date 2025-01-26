# observer.py (refatorado)

#  importação do módulo abc (Abstract Base Classes) do Python, que fornece infraestrutura para criar classes abstratas
from abc import ABC, abstractmethod

# importação do módulo typing (tipos genéricos do módulo typing):
# dict - permite especificar os tipos das chaves e valores do dicionário;
# Any - (int, str, list, etc.)

from abc import ABC, abstractmethod
from typing import Dict, Any
from utils import JSONUtils

class AnalyticsObserver(ABC):
    @abstractmethod
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        pass

# Observer Qualitativo
class QualitativeAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        qualitative_data = {
            "activity_id": activity_id,
            "student_id": student_id,
            "type": "qualitative",
            "data": {
                "acesso_atividade": data.get("acesso_atividade", False),
                "download_recursos": data.get("download_recursos", False),
                "upload_documentos": data.get("upload_documentos", False),
                "relatorio_respostas": data.get("relatorio_respostas", ""),
            },
        }
        JSONUtils.save_to_json("analytics_data", f"qualitative_{activity_id}.json", qualitative_data)
        print(f"Dados qualitativos salvos para estudante {student_id} na atividade {activity_id}")

# Observer Quantitativo
class QuantitativeAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        quantitative_data = {
            "activity_id": activity_id,
            "student_id": student_id,
            "type": "quantitative",
            "data": {
                "numero_acessos": data.get("numero_acessos", 0),
                "downloads_recursos": data.get("downloads_recursos", 0),
                "progresso_atividade": data.get("progresso_atividade", 0.0),
            },
        }
        JSONUtils.save_to_json("analytics_data", f"quantitative_{activity_id}.json", quantitative_data)
        print(f"Dados quantitativos salvos para estudante {student_id} na atividade {activity_id}")

