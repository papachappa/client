import os


CELERY_IMPORTS = ('tasks',)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SEND_TASK_SENT_EVENT = True

CELERY_BROKER_URL = os.environ.get('BROKER_URL')
if not CELERY_BROKER_URL:  
    __amqp_uri_settings = {
        'user':     os.environ.get('RABBIT_USER', 'tp_user'),
        'password': os.environ.get('RABBIT_PASSWORD', 'tp_user_password'),
        'hostname': os.environ.get('RABBIT_HOSTNAME', 'rabbit'),
        'vhost':    os.environ.get('RABBIT_VHOST', ''),
    }
    CELERY_BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        **__amqp_uri_settings
    )

CELERY_RESULT_BACKEND = CELERY_BROKER_URL

ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
    'url': os.environ.get('REDIS_URL', 'redis://redis'),
    'default_timeout': os.environ.get('ONCE_TIMEOUT', 60 * 60),
  }
}
