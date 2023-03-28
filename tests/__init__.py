from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)