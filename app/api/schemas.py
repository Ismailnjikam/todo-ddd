"""Schémas Pydantic de l'API : contrats d'entrée et de sortie d'une Tâche."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.priority import Priority
from app.domain.status import TaskStatus


class TaskInput(BaseModel):
    """Données envoyées pour créer (ou modifier) une Tâche."""

    title: str = Field(..., min_length=1, max_length=100, examples=["Faire les courses"])
    description: str = Field("", examples=["Avant midi"])
    priority: Priority = Field(Priority.MEDIUM, examples=["moyenne"])

    @field_validator("title")
    @classmethod
    def titre_non_vide(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Le titre est obligatoire.")
        return value


class TaskOutput(BaseModel):
    """Tâche renvoyée par l'API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: Priority
    status: TaskStatus
    created_at: datetime

class TaskUpdate(BaseModel):
    """Données envoyées pour modifier partiellement une Tâche (PATCH)."""

    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    priority: Priority | None = None

    @field_validator("title")
    @classmethod
    def titre_non_vide(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Le titre est obligatoire.")
        return value