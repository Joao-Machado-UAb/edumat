# singleton_db.py
from typing import Dict, Any, Optional
from datetime import datetime


class SingletonDB:
    """Serviço de gestão de base de dados com padrão Singleton"""

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._database = {}
        return cls._instance

    def create_activity(
        self,
        activity_id: str,
        resumo: str = "Resumo de equações de 7º ano",
        instrucoes: str = "https://www.matematica.pt/aulas-matematica.php?ano=7",
    ) -> Dict[str, Any]:
        """Cria uma nova atividade no banco de dados"""
        if activity_id not in self._database:
            self._database[activity_id] = {
                "resumo": resumo,
                "instrucoes": instrucoes,
                "created_at": datetime.now().isoformat(),
            }
        return self._database[activity_id]

    def update_activity(
        self,
        activity_id: str,
        resumo: Optional[str] = None,
        instrucoes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Atualiza os dados de uma atividade existente"""
        if activity_id not in self._database:
            raise KeyError(f"Atividade com ID '{activity_id}' não encontrada")

        if resumo:
            self._database[activity_id]["resumo"] = resumo
        if instrucoes:
            self._database[activity_id]["instrucoes"] = instrucoes

        self._database[activity_id]["updated_at"] = datetime.now().isoformat()
        return self._database[activity_id]

    def get_activity(self, activity_id: str) -> Optional[Dict[str, Any]]:
        """Recupera os dados de uma atividade"""
        return self._database.get(activity_id)
