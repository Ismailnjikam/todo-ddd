from app.domain.task import Task, Priority


class TaskService:
    def __init__(self, repository):
        self.repository = repository
        self.next_id = 1

    def create(self, title, description="", priority=Priority.MEDIUM):
        task = Task(self.next_id, title, description, priority)
        self.next_id += 1
        return self.repository.add(task)

    def complete(self, task_id):
        task = self._required(task_id)
        task.mark_done()
        return task

    def update(self, task_id, title, description, priority):
        task = self._required(task_id)
        task.update(title, description, priority)
        return task

    def remove(self, task_id):
        self._required(task_id)
        self.repository.delete(task_id)

    def list(self, status=None):
        tasks = self.repository.list_all()
        return [t for t in tasks if status is None or t.status.value == status]

    def _required(self, task_id):
        task = self.repository.get(task_id)
        if not task:
            raise LookupError("Tâche introuvable")
        return task