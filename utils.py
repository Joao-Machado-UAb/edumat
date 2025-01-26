# utils.py
import os
import json
from datetime import datetime

class JSONUtils:
    @staticmethod
    def save_to_json(directory: str, filename: str, data: dict) -> None:
        """Salva dados em um arquivo JSON dentro de um diretório específico."""
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)

        # Carregar dados existentes se o arquivo já existir
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Adicionar carimbo de data/hora e anexar os novos dados
        data["timestamp"] = datetime.now().isoformat()
        existing_data.append(data)

        # Salvar de volta ao arquivo
        with open(filepath, "w") as file:
            json.dump(existing_data, file, indent=4)
