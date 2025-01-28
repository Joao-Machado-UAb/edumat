# activity_manager.py

from singleton_db import SingletonDB

class ActivityManager:
    def __init__(self):
        self.db = SingletonDB()

    def create_activity(self, activity_id):
        return self.db.create_instance(activity_id)

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        return self.db.execute_operations(activity_id, resumo, instrucoes)
