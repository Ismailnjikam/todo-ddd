from abc import ABC, abstractmethod


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task): ...

    @abstractmethod
    def get(self, task_id: int): ...

    @abstractmethod
    def list_all(self): ...

    @abstractmethod
    def delete(self, task_id: int): ...