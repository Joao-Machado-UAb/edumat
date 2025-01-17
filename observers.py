# observers.py

#  importação do módulo abc (Abstract Base Classes) do Python, que fornece infraestrutura para criar classes abstratas
from abc import ABC, abstractmethod

# importação do módulo typing (tipos genéricos do módulo typing):
# List - representa uma lista e permite especificar o tipo dos elementos contidos na lista;
# dict - permite especificar os tipos das chaves e valores do dicionário;
# Any - (int, str, list, etc.)
from typing import List, Dict, Any

# Interface para o Observer
class AnalyticsObserver(ABC):
    @abstractmethod
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        pass


# Observer Concreto para Analytics Qualitativas
class QualitativeAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        # Processa e armazena analytics qualitativas
        qualitative_data = {
            "acesso_atividade": data.get("acesso_atividade", False),
            "download_recursos": data.get("download_recursos", False),
            "upload_documentos": data.get("upload_documentos", False),
            "relatorio_respostas": data.get("relatorio_respostas", ""),
        }
        print(
            f"Qualitative analytics updated for student {student_id} in activity {activity_id}"
        )
        # adicionar a lógica para guardar os dados


# Observer Concreto para Analytics Quantitativas
class QuantitativeAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        # Processa e armazena analytics quantitativas
        quantitative_data = {
            "numero_acessos": data.get("numero_acessos", 0),
            "downloads_recursos": data.get("downloads_recursos", 0),
            "progresso_atividade": data.get("progresso_atividade", 0.0),
        }
        print(
            f"Quantitative analytics updated for student {student_id} in activity {activity_id}"
        )
        # adicionar a lógica para guardar os dados


# Subject (Observable)
class ActivityAnalytics:
    def __init__(self):
        self._observers: List[AnalyticsObserver] = []

    def attach(self, observer: AnalyticsObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: AnalyticsObserver) -> None:
        self._observers.remove(observer)

    def notify(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        for observer in self._observers:
            observer.update(activity_id, student_id, data)

    def record_activity(
        self, activity_id: str, student_id: str, data: Dict[str, Any]
    ) -> None:
        # Método para registrar uma atividade e notificar os observers
        print(f"Recording activity for student {student_id} in activity {activity_id}")
        self.notify(activity_id, student_id, data)
