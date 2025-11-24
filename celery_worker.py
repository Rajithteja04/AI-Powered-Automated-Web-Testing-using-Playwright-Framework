#!/usr/bin/env python
"""
Celery worker startup script.
Run this to start the background task worker.
"""

from celery_app import celery

if __name__ == '__main__':
    celery.start()
