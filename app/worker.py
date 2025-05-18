from app.utils.celery import celery  # noqa: F401

# Import tasks so they are registered with Celery
import app.utils.tasks  # noqa: F401
