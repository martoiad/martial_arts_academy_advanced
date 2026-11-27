import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'martial_arts_academy.settings')

app = Celery('martial_arts_academy')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()