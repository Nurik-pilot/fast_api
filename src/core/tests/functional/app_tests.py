from celery import Celery
from fastapi import FastAPI

from core.celery import celery_app
from core.main import main_app


def test_celery() -> None:
    assert isinstance(celery_app, Celery)


def test_fastapi() -> None:
    assert isinstance(main_app, FastAPI)
