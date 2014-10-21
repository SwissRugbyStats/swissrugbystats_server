# starts celery for automated tasks
# configuration in crawler/celery.py
celery multi restart w1 -A crawler -B -l info
