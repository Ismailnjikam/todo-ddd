# Glossaire — langage omniprésent (contexte borné : Gestion des tâches)

| Terme | Nom dans le code | Définition |
|---|---|---|
| **Tâche** | `Task` (entité, racine d'agrégat) | Travail à accomplir par l'utilisateur. Identifiée par un `id`, avec un titre (1 à 100 caractères, obligatoire), une description facultative, une priorité, un statut et une date de création. |
| **Priorité** | `Priority` (objet-valeur) | Niveau d'importance d'une tâche. Trois valeurs figées : `basse`, `moyenne`, `élevée`. Valeur par défaut : `moyenne`. |
| **Statut** | `TaskStatus` (objet-valeur) | État d'avancement d'une tâche. Deux valeurs figées : `todo` (à faire, valeur par défaut) et `done` (terminée). |
| **Terminer une tâche** | `Task.mark_done()` | Transition unique du statut `todo` vers `done`. Une tâche déjà terminée ne peut pas être terminée une seconde fois (`TaskError`, HTTP 409). |
| **Liste des tâches** | `TaskService.list(status)` | Consultation des tâches avec titre, priorité, statut et date. Filtres : toutes, à faire (`status=todo`), terminées (`status=done`). |

Remarque : « à faire » et « terminées » sont des libellés d'affichage ; dans le code, l'API et les tests, on utilise uniquement `todo` et `done`.