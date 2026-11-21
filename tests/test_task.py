"""Tests du domaine : règles métier de la Tâche (M5 — Dupont)."""

from datetime import datetime

import pytest

from app.domain.priority import Priority
from app.domain.status import TaskError, TaskStatus
from app.domain.task import Task


def test_creation_valide():
    task = Task(id=1, title="Faire les courses", description="Avant midi")

    assert task.id == 1
    assert task.title == "Faire les courses"
    assert task.description == "Avant midi"
    assert task.priority is Priority.MEDIUM
    assert task.status is TaskStatus.TODO
    assert isinstance(task.created_at, datetime)
    assert task.created_at.tzinfo is not None


def test_titre_vide_refuse():
    with pytest.raises(TaskError):
        Task(id=1, title="")
    with pytest.raises(TaskError):
        Task(id=1, title="   ")


def test_titre_trop_long_refuse():
    with pytest.raises(TaskError):
        Task(id=1, title="a" * 101)


def test_terminer_une_tache():
    task = Task(id=1, title="Rédiger le rapport")

    task.mark_done()

    assert task.status is TaskStatus.DONE


def test_double_terminaison_refusee():
    task = Task(id=1, title="Rédiger le rapport")
    task.mark_done()

    with pytest.raises(TaskError):
        task.mark_done()

    assert task.status is TaskStatus.DONE


def test_mise_a_jour_invalide():
    task = Task(id=1, title="Titre initial", priority=Priority.HIGH)

    with pytest.raises(TaskError):
        task.update(title="")
    assert task.title == "Titre initial"

    with pytest.raises(TaskError):
        task.update(title="a" * 101)
    assert task.title == "Titre initial"

    task.update(title="Nouveau titre", description="Détails", priority=Priority.LOW)
    assert task.title == "Nouveau titre"
    assert task.description == "Détails"
    assert task.priority is Priority.LOW
