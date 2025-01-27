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

class AnalyticsObserver(ABC):
    @abstractmethod
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        pass

    def _save_to_json(self, filename: str, data: Dict[str, Any]) -> None:
        os.makedirs("analytics_data", exist_ok=True)
        filepath = f"analytics_data/{filename}"

        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        data["timestamp"] = datetime.now().isoformat()
        existing_data.append(data)

        with open(filepath, "w") as file:
            json.dump(existing_data, file, indent=4)

class UnifiedAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        analytics_data = {
            "activity_id": activity_id,
            "student_id": student_id,
            "data": {
                "acesso_atividade": data.get("acesso_atividade", False),
                "download_recursos": data.get("download_recursos", False),
                "upload_documentos": data.get("upload_documentos", False),
                "relatorio_respostas": data.get("relatorio_respostas", ""),
                "numero_acessos": data.get("numero_acessos", 0),
                "downloads_recursos": data.get("downloads_recursos", 0),
                "progresso_atividade": data.get("progresso_atividade", 0.0),
            }
        }
        self._save_to_json(f"analytics_{activity_id}.json", analytics_data)
        print(f"Dados salvos para estudante {student_id} na atividade {activity_id}")

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

    def record_activity(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        print(f"Registrando atividade para estudante {student_id} na atividade {activity_id}")
        self.notify(activity_id, student_id, data)

