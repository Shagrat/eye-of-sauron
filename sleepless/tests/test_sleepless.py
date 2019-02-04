import pytest
from flask import Flask
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client
