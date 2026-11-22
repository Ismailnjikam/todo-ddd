"""Tests des routes PUT, PATCH et DELETE /tasks/{id} (M8)."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes import get_task_service, router
from app.domain.priority import Priority
from app.domain.status import TaskError
from app.domain.task import Task

AUTRE_PRIORITE = next(p for p in Priority if p is not Priority.MEDIUM)


class FakeTaskService:
    """Faux service en mémoire, utilisé à la place de celui de Melvina."""

    def __init__(self):
        self.tasks = {1: Task(id=1, title="Faire les courses")}

    def update(self, task_id, **fields):
        task = self.tasks.get(task_id)
        if task is None:
            return None
        task.update(**fields)  # le domaine valide et lève TaskError
        return task

    def delete(self, task_id):
        return self.tasks.pop(task_id, None) is not None


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


# ---------- PATCH ----------

def test_patch_modifie_seulement_le_champ_envoye(client):
    response = client.patch("/tasks/1", json={"description": "Détail"})
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "Détail"
    assert body["title"] == "Faire les courses"  # inchangé


def test_patch_priorite(client):
    response = client.patch(
        "/tasks/1", json={"priority": AUTRE_PRIORITE.value}
    )
    assert response.status_code == 200
    assert response.json()["priority"] == AUTRE_PRIORITE.value


def test_patch_tache_introuvable_renvoie_404(client):
    response = client.patch("/tasks/999", json={"title": "x"})
    assert response.status_code == 404


def test_patch_titre_vide_renvoie_422(client):
    response = client.patch("/tasks/1", json={"title": "  "})
    assert response.status_code == 422


def test_patch_priorite_inconnue_renvoie_422(client):
    response = client.patch("/tasks/1", json={"priority": "inexistante"})
    assert response.status_code == 422


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