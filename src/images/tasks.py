from redis import Redis
import matplotlib.pyplot as plt
from celery import (
    Task,
    shared_task
)

from src.core import global_redis
from . import service


class StickingTask(Task):
    redis: Redis

    # def before_start(self, task_id, args, kwargs) -> None:
    #     redis.set(name=task_id, value=kwargs["filename"])


@shared_task(base=StickingTask, redis=global_redis, track_started=True)
def stick_images(image1: bytes, image2: bytes, filename: str) -> None:
    """:return dst"""
    print(filename)
    # kp1, desc1 = service.find_features(image1)
    # kp2, desc2 = service.find_features(image2)
    pass
