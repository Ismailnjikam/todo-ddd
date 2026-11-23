# Exemples d'utilisation de l'API

API des tâches (FastAPI). Lancement en local :

```
uvicorn app.main:app --reload
```

Adresse de base : `http://localhost:8000`.
Documentation interactive : `http://localhost:8000/docs`.

Valeurs possibles :
- `status` : `todo` ou `done`
- `priority` : valeurs de l'énumération `Priority` (par défaut : moyenne)

---

## 1. Ajouter une tâche (POST /tasks)

```
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Faire les courses", "description": "Avant midi", "priority": "moyenne"}'
```

**201 Created**
```json
{
  "id": 1,
  "title": "Faire les courses",
  "description": "Avant midi",
  "priority": "moyenne",
  "status": "todo",
  "created_at": "2026-11-23T08:00:00Z"
}
```

**422** : titre vide, trop long ou priorité inconnue
```json
{"detail": "Le titre est obligatoire."}
```

---

## 2. Consulter la liste (GET /tasks)

```
curl http://localhost:8000/tasks
curl "http://localhost:8000/tasks?status=done"
```

**200 OK**
```json
[
  {
    "id": 1,
    "title": "Faire les courses",
    "description": "Avant midi",
    "priority": "moyenne",
    "status": "todo",
    "created_at": "2026-11-23T08:00:00Z"
  }
]
```

---

## 3. Remplacer une tâche (PUT /tasks/{id})

```
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Faire les courses du soir", "description": "Après 18h", "priority": "moyenne"}'
```

**200 OK**
```json
{
  "id": 1,
  "title": "Faire les courses du soir",
  "description": "Après 18h",
  "priority": "moyenne",
  "status": "todo",
  "created_at": "2026-11-23T08:00:00Z"
}
```

**404 Not Found** : la tâche n'existe pas
```json
{"detail": "Tâche introuvable"}
```

**422 Unprocessable Entity** : titre vide, titre de plus de 100 caractères ou priorité inconnue
```json
{"detail": "Le titre ne doit pas dépasser 100 caractères."}
```

---

## 4. Terminer une tâche (PATCH /tasks/{id}/done)

```
curl -X PATCH http://localhost:8000/tasks/1/done
```

**200 OK**
```json
{
  "id": 1,
  "title": "Faire les courses du soir",
  "description": "Après 18h",
  "priority": "moyenne",
  "status": "done",
  "created_at": "2026-11-23T08:00:00Z"
}
```

**404 Not Found** : la tâche n'existe pas
```json
{"detail": "Tâche introuvable"}
```

**409 Conflict** : la tâche est déjà terminée
```json
{"detail": "La tâche est déjà terminée."}
```

---

## 5. Supprimer une tâche (DELETE /tasks/{id})

```
curl -X DELETE http://localhost:8000/tasks/1
```

**204 No Content** : la tâche est supprimée, la réponse n'a pas de corps.

**404 Not Found** : la tâche n'existe pas (ou a déjà été supprimée)
```json
{"detail": "Tâche introuvable"}
```

---

## Récapitulatif des codes

| Route | Succès | Erreurs |
|---|---|---|
| POST /tasks | 201 | 422 |
| GET /tasks | 200 | 422 (statut inconnu) |
| PUT /tasks/{id} | 200 | 404, 422 |
| PATCH /tasks/{id}/done | 200 | 404, 409 |
| DELETE /tasks/{id} | 204 | 404 |
