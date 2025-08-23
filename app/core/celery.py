"""
Celery Configuration for DocuMind™
Handles background task processing with Redis as broker
"""

from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "documind",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.document_processing",
        "app.tasks.ai_processing", 
        "app.tasks.validation_tasks",
        "app.tasks.search_tasks",
        "app.tasks.maintenance_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone
    timezone='UTC',
    enable_utc=True,
    
    # Task settings
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    task_always_eager=False,  # Set to True for testing
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    
    # Result settings
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Queue settings
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default',
    
    # Routing
    task_routes={
        'app.tasks.document_processing.*': {'queue': 'document_processing'},
        'app.tasks.ai_processing.*': {'queue': 'ai_processing'},
        'app.tasks.validation_tasks.*': {'queue': 'validation'},
        'app.tasks.search_tasks.*': {'queue': 'search'},
        'app.tasks.maintenance_tasks.*': {'queue': 'maintenance'},
    },
    
    # Beat schedule (periodic tasks)
    beat_schedule={
        'cleanup-expired-sessions': {
            'task': 'app.tasks.maintenance_tasks.cleanup_expired_sessions',
            'schedule': 3600.0,  # Every hour
        },
        'update-search-indexes': {
            'task': 'app.tasks.search_tasks.update_search_indexes',
            'schedule': 1800.0,  # Every 30 minutes
        },
        'process-pending-documents': {
            'task': 'app.tasks.document_processing.process_pending_documents',
            'schedule': 300.0,  # Every 5 minutes
        },
        'generate-embeddings-batch': {
            'task': 'app.tasks.ai_processing.generate_embeddings_batch',
            'schedule': 600.0,  # Every 10 minutes
        },
        'health-check': {
            'task': 'app.tasks.maintenance_tasks.health_check',
            'schedule': 300.0,  # Every 5 minutes
        },
    },
    
    # Security
    security_key=settings.SECRET_KEY,
    
    # Logging
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s',
)

# Optional: Configure Celery to use our custom task base
celery_app.config_from_object('app.core.celery')

if __name__ == '__main__':
    celery_app.start()
