# Wireframes - Application To-Do List (`todo-ddd`)

**Auteur :** M10 - Lorein Du Perron (UX / Design)  
**Branche :** `feature/US-00-ux`  
**Objectif :** Définir la structure visuelle et fonctionnelle des 3 écrans principaux de l'application en respectant le langage ubiquitaire DDD (*Tâche, Priorité, Statut, terminer une tâche, liste des tâches*).

---

## 1. Écran principal : Liste des tâches

Cet écran permet de consulter la **liste des tâches**, de filtrer par **Statut** (`Toutes`, `À faire` / `todo`, `Terminées` / `done`), d'accéder à la création, de **terminer une tâche** via la case à cocher, ou de déclencher la modification et la suppression.

```text
+------------------------------------------------------------------------------+

|  GESTIONNAIRE DE TÂCHES (To-Do List)                   [ + Nouvelle tâche ]  |
+------------------------------------------------------------------------------+

|                                                                              |
|  Filtres par statut :   (o) Toutes    ( ) À faire    ( ) Terminées           |
|                                                                              |
|  [ Zone de notification : ex. "Tâche créée" (succès) ou erreur 409 ]         |
|                                                                              |
|  +------------------------------------------------------------------------+  |
|  | [ ]  Finaliser les maquettes UX                    [ Priorité: élevée ]|  |
|  |      Statut : todo  |  Créée le : 22/11/2026                           |  |
|  |      Description : Rédiger wireframes.md et criteres-ux.md             |  |
|  |                                               [ Modifier ] [ Supprimer]|  |
|  +------------------------------------------------------------------------+  |
|                                                                              |
|  +------------------------------------------------------------------------+  |
|  | [x]  Initialiser le dépôt GitHub                   [ Priorité: basse ] |  |
|  |      Statut : done  |  Créée le : 20/11/2026  (Titre barré)            |  |
|  |      Description : Configuration initiale et invitation de l'équipe    |  |
|  |                                               [ Modifier ] [ Supprimer]|  |
|  +------------------------------------------------------------------------+  |
|                                                                              |
|  +------------------------------------------------------------------------+  |
|  | [ ]  Coder la feuille de style CSS                [ Priorité: moyenne ]|  |
|  |      Statut : todo  |  Créée le : 22/11/2026                           |  |
|  |                                               [ Modifier ] [ Supprimer]|  |
|  +------------------------------------------------------------------------+  |
|                                                                              |
+------------------------------------------------------------------------------+
```

### Éléments clés de l'écran 1 :
* **En-tête :** Titre de l'application et bouton d'action principal `+ Nouvelle tâche` (ouvre l'Écran 2 en mode création).
* **Barre de filtres :** Trois options exclusives (`Toutes`, `À faire` → filtre `status=todo`, `Terminées` → filtre `status=done`).
* **Carte d'une tâche :**
  * **Case à cocher (`[ ]` / `[x]`) :** Déclenche l'action *terminer une tâche* (`PATCH /tasks/{id}/done`). Une fois cochée (`done`), le titre est visuellement barré.
  * **Titre & Description :** Informations principales de la tâche.
  * **Badge de priorité :** Indicateur visuel coloré affichant exactement l'une des trois valeurs (`basse`, `moyenne`, `élevée`).
  * **Métadonnées :** Affichage explicite du **Statut** (`todo` ou `done`) et de la date de création.
  * **Actions secondaires :** Bouton `Modifier` (ouvre l'Écran 2 prérempli) et bouton `Supprimer` (ouvre l'Écran 3).

---

## 2. Écran secondaire : Formulaire de Tâche (Ajout & Modification)

Un formulaire unique s'adapte au contexte :
* **Mode Création (`POST /tasks`) :** Champs vides, priorité par défaut sur `moyenne`.
* **Mode Modification (`PUT /tasks/{id}`) :** Champs préremplis avec les données existantes de la tâche sélectionnée.

```text
+------------------------------------------------------------------------------+

|  GESTIONNAIRE DE TÂCHES - Nouvelle tâche (ou Modifier la tâche #1)           |
+------------------------------------------------------------------------------+

|                                                                              |
|  +------------------------------------------------------------------------+  |
|  |                                                                        |  |
|  |  Titre de la tâche * (1 à 100 caractères) :                            |  |
|  |  +------------------------------------------------------------------+  |  |
|  |  | Ex: Rédiger les critères d'acceptation                           |  |  |
|  |  +------------------------------------------------------------------+  |  |
|  |  [ Message d'erreur si vide : "Le titre est obligatoire." ]            |  |
|  |                                                                        |  |
|  |  Description (optionnelle) :                                           |  |
|  |  +------------------------------------------------------------------+  |  |
|  |  | Détails supplémentaires sur la tâche...                          |  |  |
|  |  |                                                                  |  |  |
|  |  +------------------------------------------------------------------+  |  |
|  |                                                                        |  |
|  |  Priorité :                                                            |  |
|  |  +--------------------------------------+                              |  |
|  |  | moyenne                       [v] |  Options : basse / moyenne / élevée
|  |  +--------------------------------------+                              |  |
|  |                                                                        |  |
|  |                                        [ Annuler ]   [ Enregistrer ]   |  |
|  +------------------------------------------------------------------------+  |
|                                                                              |
+------------------------------------------------------------------------------+
```

### Éléments clés de l'écran 2 :
* **Champ Titre (`<input type="text">`) :** Obligatoire, limité à 100 caractères (`maxlength="100"`), associé à un `<label>` explicite.
* **Champ Description (`<textarea>`) :** Facultatif, permet d'ajouter des précisions.
* **Sélecteur Priorité (`<select>`) :** Liste déroulante stricte contenant les valeurs `basse`, `moyenne`, `élevée`.
* **Boutons d'action :**
  * `Annuler` : Retourne à la **liste des tâches** sans sauvegarder.
  * `Enregistrer` : Valide les champs, appelle l'API (`POST` ou `PUT`), affiche le message de succès (`« Tâche créée »` ou `« Tâche modifiée »`) et retourne à la liste.

---

## 3. Modale de confirmation de suppression

Cette fenêtre superposée (overlay) sécurise l'action destructive de suppression (`DELETE /tasks/{id}`) afin d'éviter toute perte accidentelle de données.

```text
+------------------------------------------------------------------------------+

|  (Arrière-plan de la liste des tâches assombri / flouté)                     |
|                                                                              |
|          +--------------------------------------------------------+          |
|          |  CONFIRMER LA SUPPRESSION                              |          |
|          +--------------------------------------------------------+          |
|          |                                                        |          |
|          |  Voulez-vous vraiment supprimer cette tâche ?          |          |
|          |  "Finaliser les maquettes UX"                          |          |
|          |                                                        |          |
|          |  Cette action est irréversible.                        |          |
|          |                                                        |          |
|          |                        [ Annuler ]   [ Supprimer ]     |          |
|          +--------------------------------------------------------+          |
|                                                                              |
+------------------------------------------------------------------------------+
```

### Éléments clés de l'écran 3 :
* **Texte de confirmation :** Affiche clairement la question de confirmation ainsi que le titre de la tâche concernée.
* **Bouton `Annuler` :** Ferme immédiatement la modale sans effectuer aucun appel réseau à l'API.
* **Bouton `Supprimer` (style alerte / rouge) :** Exécute l'appel `DELETE /tasks/{id}`, ferme la modale, recharge la **liste des tâches** et affiche la notification `« Tâche supprimée »`.
