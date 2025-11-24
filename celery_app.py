from celery import Celery
from flask import current_app
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Create celery instance
celery = Celery(__name__)

# Configuration
celery.conf.broker_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
celery.conf.result_backend = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
celery.conf.task_serializer = 'json'
celery.conf.result_serializer = 'json'
celery.conf.accept_content = ['json']
celery.conf.timezone = 'UTC'
celery.conf.task_track_started = True
celery.conf.task_time_limit = 600  # 10 minutes timeout
celery.conf.task_soft_time_limit = 540  # 9 minutes soft timeout
