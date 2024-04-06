from celery import Celery

from core import global_config

celery = Celery(
    "app",
    broker=f"redis://{global_config.redis.host}:{global_config.redis.port}",
    backend=f"redis://{global_config.redis.host}:{global_config.redis.port}",
    include=[
        "src.photos.tasks"
    ],
    worker_hijack_root_logger=False
)
