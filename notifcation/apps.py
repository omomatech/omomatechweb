from django.apps import AppConfig


class NotifcationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifcation'
from django.apps import AppConfig


class NotifcationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifcation'
    def ready(self):
           from .scheduler import scheduler
           scheduler.start()