# observers.py

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
        """Método auxiliar para salvar dados em arquivo JSON"""
        # Cria o diretório 'analytics_data' caso não exista
        os.makedirs("analytics_data", exist_ok=True)

        filepath = f"analytics_data/{filename}"

        # Carrega dados existentes ou cria lista vazia
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Adiciona timestamp aos dados
        data["timestamp"] = datetime.now().isoformat()
        existing_data.append(data)

        # Guarda dados atualizados
        with open(filepath, "w") as file:
            json.dump(existing_data, file, indent=4)


class QualitativeAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        # Processa dados qualitativos
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

        # Guarda dados qualitativos
        self._save_to_json(f"qualitative_{activity_id}.json", qualitative_data)

        print(
            f"Dados qualitativos salvos para estudante {student_id} na atividade {activity_id}"
        )


class QuantitativeAnalyticsObserver(AnalyticsObserver):
    def update(self, activity_id: str, student_id: str, data: Dict[str, Any]) -> None:
        # Processa dados quantitativos
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

        # Guarda dados quantitativos
        self._save_to_json(f"quantitative_{activity_id}.json", quantitative_data)

        print(
            f"Dados quantitativos salvos para estudante {student_id} na atividade {activity_id}"
        )


# Exemplo de utilização:
if __name__ == "__main__":
    # Criar observers
    qual_observer = QualitativeAnalyticsObserver()
    quant_observer = QuantitativeAnalyticsObserver()

    # Dados para exemplo
    test_data = {
        "acesso_atividade": True,
        "download_recursos": True,
        "upload_documentos": True,
        "relatorio_respostas": "Bom desempenho",
        "numero_acessos": 5,
        "downloads_recursos": 3,
        "progresso_atividade": 75.0,
    }

    # Teste guardar
    qual_observer.update("ACT001", "STD001", test_data)
    quant_observer.update("ACT001", "STD001", test_data)
