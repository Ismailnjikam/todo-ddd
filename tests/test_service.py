import pytest
from app.application.task_service import TaskService
from app.infrastructure.in_memory_repository import InMemoryTaskRepository


@pytest.fixture
def service():
    return TaskService(InMemoryTaskRepository())


def test_create_assigns_id(service):
    t1 = service.create("Tâche 1")
    t2 = service.create("Tâche 2")
    assert t1.id == 1
    assert t2.id == 2


def test_list_returns_all_tasks(service):
    service.create("A")
    service.create("B")
    assert len(service.list()) == 2


def test_filter_by_status(service):
    a = service.create("A")
    service.create("B")
    service.complete(a.id)
    assert [t.title for t in service.list("done")] == ["A"]
    assert [t.title for t in service.list("todo")] == ["B"]


def test_missing_task_raises_lookup_error(service):
    with pytest.raises(LookupError):
        service.complete(999)


def test_remove_deletes_task(service):
    t = service.create("A")
    service.remove(t.id)
    assert service.list() == []