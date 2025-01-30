# activity_facade.py

class ActivityFacade:
    def __init__(self):
        analytics_system = ActivityAnalytics()
        analytics_system.attach(QualitativeAnalyticsObserver())
        analytics_system.attach(QuantitativeAnalyticsObserver())

        self.db = SingletonDB()
        self.activity_manager = ActivityManager(self.db)
        self.analytics_manager = AnalyticsManager(analytics_system)

    def create_activity(self, activity_id):
        return self.activity_manager.create_activity(activity_id)

    def access_activity_data(self, activity_id):
        if activity_id:
            self.analytics_manager.record_activity_access(activity_id, "student_test")
        return self.activity_manager.access_activity_data(activity_id)

    def update_activity(self, activity_id, resumo=None, instrucoes=None):
        return self.activity_manager.update_activity(activity_id, resumo, instrucoes)

    def get_analytics_list(self):
        return self.analytics_manager.get_analytics_list()

    def get_analytics_data(self):
        return self.analytics_manager.get_analytics_data()
