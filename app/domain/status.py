"""Statut d'une Tâche et erreurs métier (vocabulaire DDD : Statut)."""

from enum import Enum


class TaskStatus(str, Enum):
    """Valeurs figées : todo | done."""

    TODO = "todo"
    DONE = "done"


class TaskError(Exception):
    """Violation d'une règle métier de la Tâche."""
