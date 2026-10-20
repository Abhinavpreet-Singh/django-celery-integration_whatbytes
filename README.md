# Celery Email Project

Celery set up with Django, Redis as the broker and django-celery-results for
storing task results.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
```

Copy `.env.example` to `.env` if you want to use the email task.

## Running

```bash
docker run -d -p 6379:6379 redis:7-alpine
celery -A celery_email_project worker -l info --pool=solo
celery -A celery_email_project beat -l info
python manage.py runserver
```

Check Redis with `redis-cli ping`, it should answer PONG. `--pool=solo` is needed
on Windows or the worker takes tasks but never runs them.

## Tasks

| Task | What it does |
|------|--------------|
| `test_connection_task()` | returns a timestamp, used to check the setup works |
| `long_running_task(duration)` | sleeps, reports progress, shows async execution |
| `divide(a, b)` | retries 3 times then fails, for error handling |
| `send_email_task(recipient, subject, message)` | sends mail over SMTP |

Run them from the shell:

```python
from tasks.tasks import test_connection_task, long_running_task
test_connection_task.delay()
long_running_task.delay(10)
```

`long_running_task.delay(5)` returns in about 0.002 seconds while the task itself
takes 5, which is the point of running it in the background.

## Monitoring

Results are written to the database, so they show up in the admin at
http://localhost:8002/admin/ under Task Results with their status, return value
and traceback. Periodic schedules are under Periodic Tasks and can be changed
without restarting beat.

## Config

`celery_email_project/celery.py` creates the app and autodiscovers tasks.
Settings use `CELERY_BROKER_URL` on Redis db 0, `CELERY_RESULT_BACKEND = 'django-db'`,
timezone Asia/Kolkata with `CELERY_ENABLE_UTC = False`, and `CELERY_RESULT_EXTENDED`
so task names are saved.
