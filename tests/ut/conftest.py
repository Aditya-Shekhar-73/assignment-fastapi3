from fastapi.testclient import TestClient
from ...app.main import app
import pytest


@pytest.fixture
def client():
    '''pytest fixture for test client'''
    client = TestClient(app)
    yield client