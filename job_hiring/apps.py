from django.apps import AppConfig



class JobHiringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_hiring'

    def ready(self):
        import job_hiring.signals 
