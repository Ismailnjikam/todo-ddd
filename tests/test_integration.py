import pytest
@pytest.mark.skip(reason="En attente de la route PATCH /tasks/{id}/done (M8)")
def test_parcours_complet(client):
    # 1. Créer une tâche
    reponse = client.post("/tasks", json={"title": "Écrire le rapport"})
    assert reponse.status_code == 201
    tache = reponse.json()
    tache_id = tache["id"]

    # 2. Lister les tâches
    reponse = client.get("/tasks")
    assert reponse.status_code == 200
    assert any(t["id"] == tache_id for t in reponse.json())

    # 3. Terminer la tâche
    reponse =client.patch(f"/tasks/{tache_id}/done")
    assert reponse.status_code == 200
    assert reponse.json()["status"] == "done"

    # 4. Terminer une seconde fois : conflit
    reponse = client.patch(f"/tasks/{tache_id}/done")
    assert reponse.status_code == 409