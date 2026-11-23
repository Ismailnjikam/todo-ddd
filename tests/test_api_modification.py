"""Tests des routes PUT, PATCH /done et DELETE /tasks/{id} (M8)."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes import get_task_service, router
from app.domain.priority import Priority
from app.domain.status import TaskError, TaskStatus
from app.domain.task import Task

AUTRE_PRIORITE = next(p for p in Priority if p is not Priority.MEDIUM)


class FakeTaskService:
    def __init__(self):
        self.tasks = {1: Task(id=1, title="Faire les courses")}

    def _get(self, task_id):
        if task_id not in self.tasks:
            raise LookupError("Tâche introuvable.")
        return self.tasks[task_id]

    def update(self, task_id, title, description, priority):
        task = self._get(task_id)
        task.update(title=title, description=description,
                    priority=priority)
        return task

    def remove(self, task_id):
        self._get(task_id)
        del self.tasks[task_id]

    def complete(self, task_id):
        task = self._get(task_id)
        task.mark_done()
        return task

@pytest.fixture
def service():
    return FakeTaskService()


@pytest.fixture
def client(service):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_task_service] = lambda: service
    return TestClient(app)


# ---------- PUT ----------

def test_put_remplace_la_tache(client):
    response = client.put("/tasks/1", json={
        "title": "Nouveau titre",
        "description": "Avant midi",
        "priority": AUTRE_PRIORITE.value,
    })
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Nouveau titre"
    assert body["description"] == "Avant midi"
    assert body["priority"] == AUTRE_PRIORITE.value


def test_put_tache_introuvable_renvoie_404(client):
    response = client.put("/tasks/999", json={"title": "x"})
    assert response.status_code == 404


def test_put_titre_vide_renvoie_422(client):
    response = client.put("/tasks/1", json={"title": "   "})
    assert response.status_code == 422


def test_put_titre_trop_long_renvoie_422(client):
    response = client.put("/tasks/1", json={"title": "a" * 101})
    assert response.status_code == 422


def test_put_erreur_metier_renvoie_422(client, service):
    def refuse(task_id, **fields):
        raise TaskError("Règle métier non respectée.")

    service.update = refuse
    response = client.put("/tasks/1", json={"title": "ok"})
    assert response.status_code == 422
    assert "Règle métier" in response.json()["detail"]


# ---------- PATCH /done ----------

def test_done_renvoie_200(client):
    response = client.patch("/tasks/1/done")
    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.DONE.value


def test_done_deja_terminee_renvoie_409(client):
    client.patch("/tasks/1/done")
    assert client.patch("/tasks/1/done").status_code == 409


def test_done_introuvable_renvoie_404(client):
    assert client.patch("/tasks/999/done").status_code == 404


# ---------- DELETE ----------

def test_delete_supprime_la_tache(client, service):
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    assert 1 not in service.tasks


def test_delete_tache_introuvable_renvoie_404(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404


def test_delete_deux_fois_renvoie_404(client):
    assert client.delete("/tasks/1").status_code == 204
    assert client.delete("/tasks/1").status_code == 404