import os

from celery import Celery

if os.getenv('DOCKER', None):
    from settings import celeryconfig_docker as celeryconfig
else:
    from settings import celeryconfig


app = Celery('client')
app.config_from_object(celeryconfig, namespace='CELERY')
app.conf.ONCE = celeryconfig.ONCE
