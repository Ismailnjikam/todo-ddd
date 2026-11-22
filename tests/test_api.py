"""Tests de l'API : création et liste des tâches (M7 — Landry).

En attendant TaskService (M6) et main.py (M9), les routes sont testées avec
un service minimal qui s'appuie sur la vraie entité Task du domaine.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes import get_task_service, router
from app.domain.priority import Priority
from app.domain.status import TaskStatus
from app.domain.task import Task


class FakeTaskService:
    def __init__(self):
        self._tasks = {}
        self._next_id = 1

    def create(self, title, description="", priority=Priority.MEDIUM):
        task = Task(id=self._next_id, title=title, description=description, priority=priority)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list(self, status=None):
        tasks = list(self._tasks.values())
        if status is not None:
            tasks = [t for t in tasks if t.status is status]
        return tasks


@pytest.fixture
def service():
    return FakeTaskService()


@pytest.fixture
def client(service):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_task_service] = lambda: service
    return TestClient(app)


def test_post_cree_une_tache_201(client):
    response = client.post(
        "/tasks",
        json={"title": "Faire les courses", "description": "Avant midi", "priority": "élevée"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Faire les courses"
    assert body["description"] == "Avant midi"
    assert body["priority"] == "élevée"
    assert body["status"] == "todo"
    assert "created_at" in body


def test_post_titre_vide_422(client):
    assert client.post("/tasks", json={"title": ""}).status_code == 422
    assert client.post("/tasks", json={"title": "   "}).status_code == 422


def test_post_priorite_inconnue_422(client):
    response = client.post("/tasks", json={"title": "Tâche", "priority": "urgente"})

    assert response.status_code == 422


def test_get_liste_des_taches_200(client):
    client.post("/tasks", json={"title": "Tâche A"})
    client.post("/tasks", json={"title": "Tâche B"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["Tâche A", "Tâche B"]


def test_get_filtre_par_statut(client, service):
    client.post("/tasks", json={"title": "À faire"})
    client.post("/tasks", json={"title": "Déjà faite"})
    service._tasks[2].mark_done()

    todo = client.get("/tasks", params={"status": "todo"})
    done = client.get("/tasks", params={"status": "done"})

    assert todo.status_code == 200
    assert [t["title"] for t in todo.json()] == ["À faire"]
    assert [t["title"] for t in done.json()] == ["Déjà faite"]
    assert client.get("/tasks", params={"status": "inconnu"}).status_code == 422
