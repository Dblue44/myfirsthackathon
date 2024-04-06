from celery import shared_task
import matplotlib.pyplot as plt

from . import service


@shared_task()
def stick_photos(photo1: bytes, photos2: bytes) -> bytes:
