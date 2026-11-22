# Schéma du domaine — contexte « Gestion des tâches »

## Contexte borné
Un seul contexte : **Gestion des tâches**. Un contexte « Notifications » ou « Comptes » pourrait s'y ajouter plus tard.

## Éléments DDD

| Élément | Nom | Rôle |
|---|---|---|
| Agrégat (racine) | `Task` | Garantit les invariants : titre valide, terminer une seule fois |
| Objet-valeur | `Priority` | `basse`, `moyenne`, `élevée` ; immuable |
| Objet-valeur | `TaskStatus` | `todo`, `done` ; immuable |
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
        LOW
        MEDIUM
        HIGH
    }
    class TaskStatus {
        <<Objet-valeur>>
        TODO
        DONE
    }
    class TaskCompleted {
        <<Événement>>
        +int task_id
        +datetime completed_at
    }
    class TaskRepository {
        <<Port / interface>>
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
        +create()
        +list(status)
        +update()
        +complete()
        +remove()
    }

    Task --> Priority
    Task --> TaskStatus
    Task ..> TaskCompleted : trace optionnelle
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