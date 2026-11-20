# Répartition des tâches — To-Do List (Agile, DDD, CI/CD)

Équipe de 14 membres · Méthodologies de Développement Avancées

> Remplacez `@pseudo-github` par le compte GitHub de chaque membre.

## 0. Règles communes (valables pour TOUS)

1. **Minimum exigé par personne : 3 commits + 1 Pull Request relue par un autre membre.**
2. Une tâche = une **issue GitHub** (assignée à son responsable) → une **branche** `feature/US-XX-nom-court` → une **PR** liée à l'issue (`Closes #N`).
3. Message de commit : `US-XX: verbe + objet` (ex. `US-01: valider le titre de la tâche`).
4. Jamais de commit direct sur `main`. Fusion uniquement si : 1 approbation + CI verte.
5. Chaque PR contient : le code, le test associé, la preuve (capture ou sortie `pytest`).
6. **Definition of Done** : code relu et fusionné · test automatisé · pipeline vert · critères validés par M1 · vocabulaire DDD respecté · preuve archivée dans `docs/preuves/`.
7. Vocabulaire obligatoire (code, tests, écrans) : **Tâche, Priorité, Statut, terminer une tâche, liste des tâches**.
8. Valeurs figées : priorités `basse | moyenne | élevée` ; statuts `todo | done`.

Pour éviter les conflits Git, **chaque membre ne modifie que ses fichiers** (listés ci-dessous). Besoin de toucher un fichier d'autrui → demander au propriétaire.

## 1. Vue d'ensemble

| Groupe | Membres | Mission |
|---|---|---|
| G1 Produit & Scrum | M1 (Ismael), M2 (Armel), M3 (Florinda) | Backlog, tableau, événements Scrum, DoD |
| G2 Domaine & Application | M4 (Henrico), M5 (Dupont), M6 (Melvina) | Modèle DDD, règles métier, service |
| G3 API | M7 (Landry), M8 (Gabrielle), M9 (Girelle) | FastAPI, contrats, intégration |
| G4 Interface | M10 (Perron), M11 (Shagui), M12 (Divine) | Wireframes, formulaire, liste |
| G5 DevOps & Qualité | M13 (Michelle), M14 (Dario) | CI/CD, Docker, tests, rapport |

| Membre | Rôle | GitHub | Reviewer de sa PR |
|---|---|---|---|
| M1 — Ismael | Product Owner | @… | M3 — Florinda |
| M2 — Armel | Scrum Master | @… | M1 — Ismael |
| M3 — Florinda | Analyste Scrum | @… | M2 — Armel |
| M4 — Henrico | Lead DDD | @… | M5 — Dupont |
| M5 — Dupont | Développeur domaine | @… | M4 — Henrico |
| M6 — Melvina | Application / repository | @… | M5 — Dupont |
| M7 — Landry | API création/liste | @… | M8 — Gabrielle |
| M8 — Gabrielle | API modification | @… | M7 — Landry |
| M9 — Girelle | Intégration API | @… | M7 — Landry |
| M10 — Perron | UX / wireframes | @… | M11 — Shagui |
| M11 — Shagui | Front-end formulaire | @… | M12 — Divine |
| M12 — Divine | Front-end liste / QA | @… | M11 — Shagui |
| M13 — Michelle | DevOps | @… | M14 — Dario |
| M14 — Dario | Qualité / documentation | @… | M13 — Michelle |

Chacun doit aussi **relire au moins une PR d'un autre** (en plus de la sienne).

## 2. Backlog

| ID | Story | Critère clé | Sprint |
|---|---|---|---|
| US-01 | Ajouter une tâche | Titre vide refusé ; tâche visible après création | 1 |
| US-02 | Consulter les tâches | Titre, priorité, statut, date visibles | 1 |
| US-03 | Terminer une tâche | Statut changé ; double clôture refusée (409) | 1 |
| US-08 | Exécuter la CI | Tests lancés à chaque push | 1 |
| US-04 | Modifier une tâche | Valeurs mises à jour et validées | 2 |
| US-05 | Supprimer une tâche | Confirmation puis disparition | 2 |
| US-06 | Choisir une priorité | Trois valeurs, badge affiché | 2 |
| US-07 | Filtrer les tâches | Toutes / à faire / terminées | 2 |
| US-09 | Lancer par Docker | Image construite, appli disponible | 2 |

## 3. Tâches détaillées par membre

### M1 — Ismael : Product Owner
**Fichiers :** `docs/backlog.md`, `docs/criteres-acceptation.md`, `docs/script-demo.md`
**Branche :** `feature/US-00-backlog-po`

1. Copier le backlog ci-dessus dans `docs/backlog.md`, y ajouter priorité (1 à 9) et points (Sprint 1 = 12 pts, Sprint 2 = 13 pts). *(commit 1)*
2. Pour chaque story, écrire dans `docs/criteres-acceptation.md` 2 à 3 critères au format « Étant donné… Quand… Alors… ». *(commit 2)*
3. Écrire `docs/script-demo.md` : déroulé de la démo finale (parcours A, B, C — voir conception §7), minuté. *(commit 3)*
4. Pendant tout le projet : **valider chaque story** en commentant la PR (« Critères OK ») et rédiger un compte-rendu de review par sprint dans `docs/scrum/review-sprint-N.md`.

**Preuves :** backlog versionné, 9 validations, 2 comptes-rendus de review.

### M2 — Armel : Scrum Master
**Fichiers :** `docs/scrum/planning-sprint-1.md`, `planning-sprint-2.md`, `retro-sprint-1.md`, `retro-sprint-2.md`, `burndown.md`
**Branche :** `feature/US-00-scrum-events`

1. Créer le tableau **GitHub Projects** (colonnes : Backlog · À faire · En cours · En revue · Terminé) et y ajouter toutes les issues. *(preuve : capture)*
2. Animer et documenter le **planning du sprint 1**, puis du sprint 2 (objectif, stories, répartition). *(commit 1 et 2)*
3. Animer un **daily** par jour (15 min) ; noter blocages dans `docs/scrum/dailies.md`. *(commit 3)*
4. Après chaque sprint : rétro (ce qui a bien/mal marché + 2 actions) et mise à jour du `burndown.md` (points restants par jour).

**Preuves :** 2 plannings, 2 reviews, 2 rétros, burndown.

### M3 — Florinda : Analyste Scrum
**Fichiers :** `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/tache.md`, `docs/dod.md`, `docs/tracabilite.md`
**Branche :** `feature/US-00-dod-templates`

1. Rédiger `docs/dod.md` (copier la DoD de la section 0 et la détailler). *(commit 1)*
2. Créer le **template de PR** avec checklist : story liée · test ajouté · CI verte · capture jointe · vocabulaire DDD · reviewer ≠ auteur. *(commit 2)*
3. Créer le template d'issue + `docs/tracabilite.md` (tableau Story → Issue → Branche → PR → Test → Preuve). *(commit 3)*
4. Tenir à jour le tableau de traçabilité et contrôler qu'aucune carte n'est « Terminé » sans preuve.

**Preuves :** DoD adoptée, tableau à jour, checklist remplie sur chaque PR.

### M4 — Henrico : Lead DDD
**Fichiers :** `docs/ddd/glossaire.md`, `docs/ddd/schema-domaine.md`, `app/domain/events.py`
**Branche :** `feature/US-00-modele-ddd`

1. `docs/ddd/glossaire.md` : définir Tâche, Priorité, Statut, terminer une tâche, liste des tâches. *(commit 1)*
2. `docs/ddd/schema-domaine.md` : contexte borné « Gestion des tâches », agrégat `Task`, objets-valeur `Priority`/`TaskStatus`, port `TaskRepository`, service `TaskService`, événement `TaskCompleted` (diagramme Mermaid). *(commit 2)*
3. `app/domain/events.py` : dataclass `TaskCompleted(task_id: int, completed_at: datetime)`. *(commit 3)*
4. Relire toutes les PR pour vérifier les noms métier et que le **domaine n'importe ni FastAPI ni infrastructure**.

**Preuves :** schéma DDD, glossaire, PR de revue domaine.

### M5 — Dupont : Développeur domaine
**Fichiers :** `app/domain/priority.py`, `app/domain/status.py`, `app/domain/task.py`, `tests/test_task.py`
**Branche :** `feature/US-01-domaine-task`

1. `priority.py` (`Priority`: LOW=basse, MEDIUM=moyenne, HIGH=élevée) et `status.py` (`TaskStatus`: TODO=todo, DONE=done) + `TaskError`. *(commit 1)*
2. `task.py` : dataclass `Task` (id, title, description, priority, status, created_at), validation du titre (1–100 caractères), `update()`, `mark_done()` (erreur si déjà terminée). **TDD : écrire d'abord les tests (rouges).** *(commit 2)*
3. `tests/test_task.py` — **6 tests** : création valide · titre vide · titre > 100 · terminaison · double terminaison · mise à jour invalide. *(commit 3)*
4. Utiliser `datetime.now(timezone.utc)` plutôt que `utcnow()` (déprécié).

**Preuves :** 6 tests domaine verts (sortie `pytest`).

### M6 — Melvina : Application / repository
**Fichiers :** `app/domain/repository.py`, `app/infrastructure/in_memory_repository.py`, `app/application/task_service.py`, `tests/test_service.py`
**Branche :** `feature/US-02-service-repository`

1. `repository.py` : classe abstraite `TaskRepository` (`add`, `get`, `list_all`, `delete`). *(commit 1)*
2. `in_memory_repository.py` : `InMemoryTaskRepository` basé sur un dict. *(commit 2)*
3. `task_service.py` : `TaskService` (`create`, `complete`, `update`, `remove`, `list(status)`, `_required` → `LookupError`), attribution des identifiants. *(commit 3)*
4. `tests/test_service.py` — **5 tests** : création affecte un id · liste · filtre · tâche absente · suppression.

**Dépend de :** M5 (fusionner après la PR de M5, ou travailler en parallèle avec un `Task` provisoire).
**Preuves :** 5 tests de service verts.

### M7 — Landry : API création / liste
**Fichiers :** `app/api/schemas.py`, `app/api/routes.py` (routes POST et GET uniquement), `tests/test_api.py` (tests POST/GET)
**Branche :** `feature/US-01-api-create-list`

1. `schemas.py` : `TaskInput` (title 1–100, description, priority) et `TaskOutput` (Pydantic). *(commit 1)*
2. Routes `POST /tasks` (201 / 422) et `GET /tasks?status=todo|done` (200). *(commit 2)*
3. Tests : POST 201 · POST 422 (titre vide) · GET 200 · GET filtré. Vérifier Swagger `/docs`. *(commit 3)*
4. Convention conflits : M7 crée `routes.py` en premier ; M8 ajoute ses routes après la fusion.

**Preuves :** tests 201/200/422 + capture de `/docs`.

### M8 — Gabrielle : API modification
**Fichiers :** `app/api/routes.py` (routes PUT, PATCH, DELETE), `docs/api-exemples.md`, `tests/test_api.py` (tests PUT/PATCH/DELETE)
**Branche :** `feature/US-03-api-update-done-delete`

1. `PUT /tasks/{id}` (200/404/422) avec les mêmes validations qu'à la création. *(commit 1)*
2. `PATCH /tasks/{id}/done` (200/404/**409** si déjà terminée) et `DELETE /tasks/{id}` (204/404). *(commit 2)*
3. `docs/api-exemples.md` : exemples `curl` et réponses JSON pour chaque route. *(commit 3)*
4. Tests : PUT 200 · PATCH 200 · PATCH 409 · DELETE 204 · DELETE 404.

**Dépend de :** M7 (fusion de la PR de M7 d'abord).
**Preuves :** tests 200/204/404/409.

### M9 — Girelle : Intégration API
**Fichiers :** `app/main.py`, `app/api/dependencies.py`, `tests/conftest.py`, `tests/test_integration.py`
**Branche :** `feature/US-02-integration-main`

1. `dependencies.py` : instance unique de `InMemoryTaskRepository` + `TaskService` injectée dans les routes. *(commit 1)*
2. `main.py` : `FastAPI()`, inclusion du routeur, service des fichiers `static/` à la racine `/`. *(commit 2)*
3. `conftest.py` (fixture `client` = `TestClient` avec dépôt réinitialisé entre les tests) + `test_integration.py` : parcours complet créer → lister → terminer → 409. *(commit 3)*
4. Vérifier le contrat JSON stable et l'absence de couplage infrastructure → domaine.

**Preuves :** suite API verte, `uvicorn app.main:app` démarre.

### M10 — Perron : UX / wireframes
**Fichiers :** `docs/ux/wireframes.md`, `docs/ux/criteres-ux.md`, `static/css/style.css`
**Branche :** `feature/US-00-ux`

1. Reprendre les 3 écrans (liste, formulaire, confirmation de suppression) dans `docs/ux/wireframes.md`. *(commit 1)*
2. `criteres-ux.md` : états chargement / vide / erreur / succès, messages exacts (« Aucune tâche pour ce filtre. Créez votre première tâche. », « Tâche créée / modifiée / supprimée », « La tâche est déjà terminée »), accessibilité. *(commit 2)*
3. `style.css` : styles de cartes, badges de priorité (3 couleurs), boutons, modale, contraste suffisant. *(commit 3)*
4. Faire valider la navigation par M1.

**Preuves :** wireframes approuvés par M1, liste de critères UX.

### M11 — Shagui : Front-end formulaire
**Fichiers :** `static/js/api.js`, `static/js/form.js`
**Branche :** `feature/US-01-front-form`

1. `api.js` : fonctions `createTask`, `updateTask`, `completeTask`, `deleteTask`, `listTasks(status)` (fetch + gestion d'erreurs). *(commit 1)*
2. `form.js` : formulaire Ajouter/Modifier (titre ≤ 100, description, priorité), libellés associés, message « Le titre est obligatoire. » *(commit 2)*
3. Mode modification : préremplissage + `PUT` ; mode création : `POST` ; message de succès puis retour à la liste. *(commit 3)*

**Preuves :** captures/vidéo des parcours US-01 et US-04.

### M12 — Divine : Front-end liste / QA
**Fichiers :** `static/index.html`, `static/js/list.js`, `docs/preuves/parcours-manuels.md`
**Branche :** `feature/US-02-front-list`

1. `index.html` : structure de la page, liens vers `style.css`, `api.js`, `form.js`, `list.js`, conteneurs liste/filtres/modale. *(commit 1)*
2. `list.js` : cartes (titre, priorité en badge, statut, date), filtres Toutes/À faire/Terminées, case à cocher → `PATCH done`, affichage du message 409. *(commit 2)*
3. Modale de confirmation de suppression (Annuler = aucun appel API ; Supprimer = `DELETE` + message + rechargement). *(commit 3)*
4. QA : exécuter manuellement les parcours A, B, C et consigner résultats + captures dans `docs/preuves/parcours-manuels.md`.

**Preuves :** parcours US-02/03/05/06/07 capturés.

### M13 — Michelle : DevOps
**Fichiers :** `Dockerfile`, `.dockerignore`, `.github/workflows/ci.yml`, `requirements.txt`, `.gitignore`
**Branche :** `feature/US-08-ci-docker`

1. Dépôt GitHub créé, collaborateurs invités, **protection de `main`** (PR obligatoire, 1 approbation, CI verte). *(préparé en amont, voir guide)*
2. `ci.yml` : job `test` (pytest) puis job `docker` (build). *(commit 1)*
3. `Dockerfile` + `.dockerignore` ; vérifier `docker build -t todo-app .` puis `docker run -p 8000:8000 todo-app`. *(commit 2)*
4. Démonstration **pipeline vert → rouge → corrigé** : branche `demo/ci-rouge` avec un test cassé volontairement, capture de l'échec, correction, capture du vert. *(commit 3)*
5. Aucun secret versionné.

**Preuves :** `ci.yml`, image qui démarre, 3 captures Actions (vert, rouge, corrigé).

### M14 — Dario : Qualité / documentation
**Fichiers :** `README.md`, `docs/strategie-test.md`, `docs/rapport-qualite.md`, `docs/preuves/checklist-finale.md`
**Branche :** `feature/US-00-qualite-doc`

1. `docs/strategie-test.md` : matrice des **12 tests** (domaine 6 / service 5 / API ≥ 5) et niveaux de test. *(commit 1)*
2. `README.md` exécutable : prérequis, installation, `pytest`, lancement local (`uvicorn`), Docker, structure du dépôt. *(commit 2)*
3. `rapport-qualite.md` + `checklist-finale.md` : nombre de tests, couverture, revues de PR, état du pipeline. *(commit 3)*
4. Vérifier que ≥ 10 tests passent et que chaque membre a 3 commits + 1 PR relue (onglet *Insights → Contributors*).

**Preuves :** rapport de qualité, README testé sur machine propre, checklist finale.

## 4. Ordre de fusion conseillé (dépendances)

```
M13 (CI) ─┐
M5 → M6 ──┼→ M7 → M8 → M9 ──→ M12 / M11 (front) → M14 (rapport final)
M4, M10, M1–M3 : en parallèle (docs)
```

## 5. Planning condensé (version rapide)

| Moment | Objectif |
|---|---|
| **Vendredi soir** | Dépôt initialisé, membres invités, issues créées, planning Sprint 1 (M1–M3, M13) |
| **Samedi matin** | Domaine + service (M4–M6), wireframes (M10) |
| **Samedi après-midi** | API (M7–M9), formulaire + liste (M11, M12), CI (M13) → **Sprint 1 : US-01/02/03/08 fusionnées** |
| **Samedi soir** | Review + rétro Sprint 1 (M1–M3) |
| **Dimanche matin** | Sprint 2 : PUT, DELETE, priorité, filtre, Docker (US-04/05/06/07/09) |
| **Dimanche après-midi** | Démo CI rouge/vert, README, rapport, captures, review + rétro finales |

## 6. Checklist finale

- [ ] Les 5 fonctions métier marchent (créer, consulter, modifier, supprimer, terminer) ; filtres et priorités visibles
- [ ] Couches `domain`, `application`, `infrastructure`, `api` séparées
- [ ] ≥ 10 tests verts ; pipeline vert / rouge / corrigé capturés
- [ ] `docker build` puis `docker run` démarrent l'application
- [ ] Aucun secret versionné
- [ ] 14 membres : ≥ 3 commits + 1 PR relue chacun
- [ ] Événements Scrum documentés (plannings, dailies, reviews, rétros, burndown)
- [ ] Livrables de démo : lien GitHub, tableau Scrum, backlog, schéma DDD, captures pipeline, historique de PR, image Docker, captures des parcours A/B/C