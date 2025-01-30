# activity_manager.py

class ActivityManager:
    def __init__(self, db):
        self.db = db

    def create_activity(self, activity_id):
        return self.db.create_instance(activity_id)

    def access_activity_data(self, activity_id):
        return self.db.access_data(activity_id)

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        return self.db.execute_operations(activity_id, resumo, instrucoes)
