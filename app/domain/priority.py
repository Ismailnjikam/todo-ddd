"""Priorité d'une Tâche (vocabulaire DDD : Priorité)."""

from enum import Enum


class Priority(str, Enum):
    """Valeurs figées : basse | moyenne | élevée."""

    LOW = "basse"
    MEDIUM = "moyenne"
    HIGH = "élevée"
