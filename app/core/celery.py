from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "doc_processing",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.document_processing",
        "app.tasks.ai_processing",
        "app.tasks.validation_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.PROCESSING_TIMEOUT,
    task_soft_time_limit=settings.PROCESSING_TIMEOUT - 30,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    broker_connection_retry_on_startup=True,
)

# Optional: Configure task routing
celery_app.conf.task_routes = {
    "app.tasks.document_processing.*": {"queue": "document_processing"},
    "app.tasks.ai_processing.*": {"queue": "ai_processing"},
    "app.tasks.validation_tasks.*": {"queue": "validation"},
}

if __name__ == "__main__":
    celery_app.start()
