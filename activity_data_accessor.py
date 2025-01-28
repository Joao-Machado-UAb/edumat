# activity_data_accessor.py

from singleton_db import SingletonDB
from observer import ActivityAnalytics

class ActivityDataAccessor:
    def __init__(self):
        self.db = SingletonDB()
        self.analytics = ActivityAnalytics()

    def access_activity_data(self, activity_id):
        if activity_id:
            self.analytics.record_activity(
                activity_id,
                "student_test",
                {"acesso_atividade": True, "numero_acessos": 1},
            )
        return self.db.access_data(activity_id)
