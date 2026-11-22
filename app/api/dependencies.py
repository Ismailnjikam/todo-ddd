from app.application.task_service import TaskService
from app.infrastructure.in_memory_repository import InMemoryTaskRepository

# Une seule instance, partagée par toutes les routes
_repository = InMemoryTaskRepository()
_service = TaskService(_repository)


def get_repository() -> InMemoryTaskRepository:
    return _repository


def get_task_service() -> TaskService:
    return _service