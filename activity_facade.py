# activity_facade.py (refatorado)

from activity_manager import ActivityManager
from analytics_manager import AnalyticsManager
from activity_data_accessor import ActivityDataAccessor

class ActivityFacade:
    def __init__(self):
        self.activity_manager = ActivityManager()
        self.analytics_manager = AnalyticsManager()
        self.activity_data_accessor = ActivityDataAccessor()

    def create_activity(self, activity_id):
        return self.activity_manager.create_activity(activity_id)

    def access_activity_data(self, activity_id):
        return self.activity_data_accessor.access_activity_data(activity_id)

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        return self.activity_manager.update_activity(activity_id, resumo, instrucoes)

    def get_analytics_list(self):
        return self.analytics_manager.get_analytics_list()

    def get_analytics_data(self):
        return self.analytics_manager.get_analytics_data()
