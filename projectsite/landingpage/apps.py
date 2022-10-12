from django.apps import AppConfig


class LandingpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landingpage'

    def ready(self):
        from jobs import updater
        updater.start()

# class MainConfig(AppConfig):
#     name = 'landingpage'

#     def ready(self):
#     	from jobs import updater
#     	updater.start()