# Critères UX, États d'Interface et Accessibilité (`todo-ddd`)

**Auteur :** M10 - Lorein Du Perron (UX / Design)  
**Branche :** `feature/US-00-ux`  
**Destinataires :** M11 (Front-end formulaire), M12 (Front-end liste / QA), M1 (Product Owner)  
**Objectif :** Définir les règles d'interaction, les 4 états de l'interface, les messages textuels exacts et les normes d'accessibilité.

---

## 1. Les 4 états de l'interface utilisateur

Toute vue de l'application doit gérer explicitement ces 4 états pour garantir un retour visuel clair à l'utilisateur :

| État | Déclencheur | Comportement visuel attendu |
| :--- | :--- | :--- |
| **1. Chargement** | Appel API en cours (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) | Affichage d'un indicateur de chargement discret (*« Chargement des tâches... »*) et désactivation temporaire des boutons de soumission pour éviter les doubles envois. |
| **2. Liste vide** | Réponse `200 OK` avec un tableau vide `[]` (aucune tâche ou aucune tâche pour le filtre actif) | Masquage de la liste et affichage centré du message d'invitation à créer une tâche. |
| **3. Erreur** | Validation front-end échouée ou code retour HTTP `404` / `409` / `422` / `500` | Affichage d'un bandeau ou message d'alerte rouge très contrasté, avec icône d'avertissement et conservation des données saisies dans le formulaire. |
| **4. Succès** | Action validée par l'API (`201 Created`, `200 OK`, `204 No Content`) | Affichage d'une notification verte temporaire (auto-fermeture après 3 à 4 secondes ou fermable manuellement) et rafraîchissement immédiat de la liste. |

---

## 2. Messages textuels exacts imposés

Afin d'assurer l'uniformité avec les critères d'acceptation et les tests automatisés/manuels (QA), **aucune reformulation n'est autorisée** pour les messages suivants :

### Notifications et états de liste
* **Liste vide (aucune tâche trouvée) :**
  > `Aucune tâche pour ce filtre. Créez votre première tâche.`
* **Succès après création (`POST /tasks` → `201`) :**
  > `Tâche créée`
* **Succès après modification (`PUT /tasks/{id}` → `200`) :**
  > `Tâche modifiée`
* **Succès après suppression (`DELETE /tasks/{id}` → `204`) :**
  > `Tâche supprimée`

### Messages d'erreur (Validation et Règles métier)
* **Erreur titre vide ou uniquement composé d'espaces :**
  > `Le titre est obligatoire.`
* **Erreur double clôture d'une tâche déjà terminée (`PATCH /tasks/{id}/done` → HTTP `409 Conflict`) :**
  > `La tâche est déjà terminée`

---

## 3. Vocabulaire métier et valeurs figées

Conformément au glossaire DDD du projet, l'interface doit exclusivement employer :
* **Termes autorisés :** *Tâche*, *Priorité*, *Statut*, *terminer une tâche*, *liste des tâches*.
* **Valeurs de Priorité (avec code couleur distinct) :**
  * `basse` : Badge ton neutre / vert doux (faible urgence).
  * `moyenne` : Badge ton ambre / jaune-orangé (urgence normale).
  * `élevée` : Badge ton rouge / corail (urgence haute).
* **Valeurs de Statut :**
  * `todo` (affiché dans les filtres sous le libellé *À faire*).
  * `done` (affiché dans les filtres sous le libellé *Terminées*, avec titre barré sur la carte).

---

## 4. Critères d'accessibilité (WCAG 2.1 Niveau AA)

1. **Contrastes des couleurs :**
   * Ratio de contraste minimal de **4.5:1** entre le texte et son arrière-plan (notamment sur les badges de priorité `basse`, `moyenne`, `élevée` et les bandeaux d'alerte).
   * L'information de priorité ne repose jamais uniquement sur la couleur : le texte exact (`basse`, `moyenne`, `élevée`) est toujours écrit en clair dans le badge.
2. **Formulaire et étiquetage :**
   * Chaque champ de saisie (`input`, `textarea`, `select`) possède une balise `<label for="...">` explicitement liée à son attribut `id`.
   * Les messages d'erreur sont annoncés via un attribut `role="alert"` ou `aria-live="polite"`.
3. **Navigation au clavier et Focus :**
   * Tous les éléments interactifs (filtres, cases à cocher, boutons `Modifier`, `Supprimer`, `Annuler`, `Enregistrer`) sont accessibles via la touche `Tab`.
   * Un contour de focus (`:focus-visible`) bien visible entoure l'élément actif.
4. **Modale de confirmation de suppression :**
   * À l'ouverture de la modale (`role="dialog"`, `aria-modal="true"`), le focus est déplacé sur le bouton `Annuler` par sécurité, et la touche `Échap` permet de fermer la modale sans supprimer.
