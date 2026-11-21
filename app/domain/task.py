"""Entité du domaine : la Tâche et ses règles métier.

Le domaine ne dépend ni de FastAPI ni de l'infrastructure.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.priority import Priority
from app.domain.status import TaskError, TaskStatus

MAX_TITLE_LENGTH = 100


def _validate_title(title: str) -> None:
    if not isinstance(title, str) or not title.strip():
        raise TaskError("Le titre est obligatoire.")
    if len(title) > MAX_TITLE_LENGTH:
        raise TaskError("Le titre ne doit pas dépasser 100 caractères.")


def _coerce_priority(priority: Priority | str) -> Priority:
    try:
        return Priority(priority)
    except ValueError as exc:
        raise TaskError("Priorité inconnue.") from exc


@dataclass
class Task:
    """Agrégat Tâche : identité, titre, description, priorité, statut et date."""

    id: int | None
    title: str
    description: str = ""
    priority: Priority | str = Priority.MEDIUM
    status: TaskStatus | str = TaskStatus.TODO
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        _validate_title(self.title)
        self.priority = _coerce_priority(self.priority)
        try:
            self.status = TaskStatus(self.status)
        except ValueError as exc:
            raise TaskError("Statut inconnu.") from exc

    def update(
        self,
        title: str | None = None,
        description: str | None = None,
        priority: Priority | str | None = None,
    ) -> None:
        """Modifier la Tâche ; toute valeur invalide est refusée avant mutation."""
        if title is not None:
            _validate_title(title)
        new_priority = _coerce_priority(priority) if priority is not None else None

        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if new_priority is not None:
            self.priority = new_priority

    def mark_done(self) -> None:
        """Terminer la Tâche ; une double clôture est refusée."""
        if self.status is TaskStatus.DONE:
            raise TaskError("La tâche est déjà terminée.")
        self.status = TaskStatus.DONE
