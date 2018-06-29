from . import utils


CELERY_IMPORTS = ('tasks',)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SEND_TASK_SENT_EVENT = True

__settings = utils.get_settings()

CELERY_BROKER_URL = __settings['BROKER_URL']
CELERY_RESULT_BACKEND = __settings['RESULT_BACKEND']

del __settings

ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': 'redis://localhost:6379/0',
    'default_timeout': 60 * 60
  }
}
