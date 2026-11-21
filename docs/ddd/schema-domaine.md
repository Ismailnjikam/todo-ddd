# Schéma du domaine — contexte « Gestion des tâches »

## Contexte borné
Un seul contexte : **Gestion des tâches**. Un contexte « Notifications » ou « Comptes » pourrait s'y ajouter plus tard.

## Éléments DDD

| Élément | Nom | Rôle |
|---|---|---|
| Agrégat (racine) | `Task` | Garantit les invariants : titre valide, terminer une seule fois |
| Objet-valeur | `Priority` | `basse`, `moyenne`, `élevée` ; immuable |
| Objet-valeur | `TaskStatus` | `à faire`, `terminée` ; immuable |
| Port (interface) | `TaskRepository` | Accès aux tâches sans connaître le stockage |
| Service applicatif | `TaskService` | Orchestre les cas d'usage |
| Événement | `TaskCompleted` | Émis quand une tâche est terminée |

## Diagramme

```mermaid
classDiagram
    class Task {
        <<Entité / racine d'agrégat>>
        +int id
        +str title
        +str description
        +Priority priority
        +TaskStatus status
        +datetime created_at
        +mark_done()
        +update(title, description, priority)
    }
    class Priority {
        <<Objet-valeur>>
        BASSE
        MOYENNE
        ELEVEE
    }
    class TaskStatus {
        <<Objet-valeur>>
        A_FAIRE
        TERMINEE
    }
    class TaskCompleted {
        <<Événement>>
        +int task_id
        +datetime completed_at
    }
    class TaskRepository {
        <<Port / interface>>
        +next_id()
        +add(task)
        +get(task_id)
        +list_all()
        +delete(task_id)
    }
    class InMemoryTaskRepository {
        <<Infrastructure>>
    }
    class TaskService {
        <<Service applicatif>>
        +add_task()
        +list_tasks(status)
        +update_task()
        +complete_task()
        +delete_task()
    }

    Task --> Priority
    Task --> TaskStatus
    Task ..> TaskCompleted : émet
    TaskRepository ..> Task : persiste
    InMemoryTaskRepository ..|> TaskRepository : implémente
    TaskService --> TaskRepository : utilise
    TaskService ..> Task : orchestre
```

## Règle de dépendance
Le **domaine ne dépend de rien** : ni FastAPI, ni infrastructure. Les autres couches dépendent de lui, jamais l'inverse.

```
API → Application → Domaine ← Infrastructure
```