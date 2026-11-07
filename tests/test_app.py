import pytest
from app.app import app, tasks


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        tasks.clear()
        tasks.extend([
            {"id": 1, "title": "Configurer Docker", "completed": True},
            {"id": 2, "title": "Créer pipeline CI/CD", "completed": False}
        ])

        yield client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["application"] == "TaskManager API"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json) == 2


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Apprendre GitHub Actions"}
    )

    assert response.status_code == 201
    assert response.json["title"] == "Apprendre GitHub Actions"


def test_create_task_without_title(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 400
