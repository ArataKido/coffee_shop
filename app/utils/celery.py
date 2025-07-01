from celery import Celery

from app.config import Config

config = Config()
celery = Celery(__name__)
celery.conf.broker_url = config.redis.redis_url
celery.conf.result_backend = config.redis.redis_url
