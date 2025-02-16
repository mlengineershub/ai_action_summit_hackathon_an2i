from celery import Celery

celery = Celery(
    'medical_api',
    broker='redis://redis:6379/0',  # Use service name 'redis' instead of 'localhost'
    backend='redis://redis:6379/1',
    include=['workspace.src.tasks']  # Add tasks module to include list
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Paris',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour timeout
    worker_prefetch_multiplier=1,  # One task per worker at a time
    task_routes={
        'workspace.src.tasks.detect_anomalies_task': {'queue': 'llm'},
        'workspace.src.tasks.generate_report_task': {'queue': 'llm'},
        'workspace.src.tasks.search_articles_task': {'queue': 'api'},
        'workspace.src.tasks.generate_search_summary_task': {'queue': 'llm'},
    }
)