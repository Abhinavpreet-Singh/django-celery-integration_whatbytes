import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_task(self, recipient, subject, message):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
    except Exception as exc:
        logger.error('Email to %s failed: %s', recipient, exc)
        raise self.retry(exc=exc, countdown=30)

    logger.info('Email sent to %s', recipient)
    return f'sent to {recipient}'
