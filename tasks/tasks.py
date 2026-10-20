import logging
import time

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def test_connection_task():
    now = timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('Connection test ran at %s', now)
    return {'status': 'connected', 'ran_at': now}


@shared_task(bind=True)
def long_running_task(self, duration=10):
    logger.info('Sleeping for %s seconds', duration)

    for second in range(duration):
        time.sleep(1)
        self.update_state(state='PROGRESS', meta={'elapsed': second + 1, 'duration': duration})

    logger.info('Finished after %s seconds', duration)
    return {'status': 'done', 'duration': duration}


@shared_task(bind=True, max_retries=3)
def divide(self, a, b):
    try:
        return a / b
    except ZeroDivisionError as exc:
        logger.error('Cannot divide %s by zero', a)
        raise self.retry(exc=exc, countdown=5)
