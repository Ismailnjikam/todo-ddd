from app.domain.repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks = {}

    def add(self, task):
        self.tasks[task.id] = task
        return task

    def get(self, task_id):
        return self.tasks.get(task_id)

    def list_all(self):
        return list(self.tasks.values())

    def delete(self, task_id):
        return self.tasks.pop(task_id, None)