def test_parcours_complet(client):
    # 1. Créer
    reponse = client.post("/tasks", json={"title": "Écrire le rapport"})
    assert reponse.status_code == 201
    tache = reponse.json()
    tache_id = tache["id"]

    # 2. Lister
    reponse = client.get("/tasks")
    assert reponse.status_code == 200
    assert any(t["id"] == tache_id for t in reponse.json())

    # 3. Terminer
    reponse = client.post(f"/tasks/{tache_id}/complete")
    assert reponse.status_code == 200
    assert reponse.json()["status"] == "done"

    # 4. Terminer une seconde fois : conflit
    reponse = client.post(f"/tasks/{tache_id}/complete")
    assert reponse.status_code == 409