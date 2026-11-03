import pytest
from app import create_app

@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test_taskflow.sqlite3"
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret", "DATABASE": str(db_path)})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
