from celery import Celery

from app.config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.redis_url
celery.conf.result_backend = settings.redis_url
