"""Événement du domaine : trace qu'une tâche vient d'être terminée."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class TaskCompleted:
    task_id: int
    completed_at: datetime = field(default_factory=datetime.now)