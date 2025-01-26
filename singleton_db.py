# singleton_db.py
from typing import Dict, Any, Optional
from datetime import datetime


class SingletonDB:
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
        if activity_id not in self._database:
            self._database[activity_id] = {
                "resumo": resumo,
                "instrucoes": instrucoes,
                "created_at": datetime.now().isoformat(),
                "analytics": {"qualitative": [], "quantitative": []},
            }
        return self._database[activity_id]

    def update_activity(
        self,
        activity_id: str,
        resumo: Optional[str] = None,
        instrucoes: Optional[str] = None,
    ) -> Dict[str, Any]:
        if activity_id not in self._database:
            raise KeyError(f"Atividade com ID '{activity_id}' não encontrada")

        if resumo:
            self._database[activity_id]["resumo"] = resumo
        if instrucoes:
            self._database[activity_id]["instrucoes"] = instrucoes

        self._database[activity_id]["updated_at"] = datetime.now().isoformat()
        return self._database[activity_id]

    def record_analytics(
        self, activity_id: str, analytics_type: str, data: Dict[str, Any]
    ):
        if activity_id not in self._database:
            raise KeyError(f"Atividade com ID '{activity_id}' não encontrada")

        self._database[activity_id]["analytics"][analytics_type].append(
            {"timestamp": datetime.now().isoformat(), "data": data}
        )
