"""Routes HTTP de la liste des tâches.

M7 (Landry) : POST /tasks et GET /tasks.
M8 (Gabrielle) ajoute PUT, PATCH et DELETE à la suite, après fusion.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas import TaskInput, TaskOutput
from app.domain.status import TaskError, TaskStatus

router = APIRouter(prefix="/tasks", tags=["Tâches"])


def get_task_service():
    """Fournit le TaskService unique défini par M9 dans app/api/dependencies.py.

    Import différé : les routes restent importables tant que la PR de M9
    n'est pas fusionnée. Les tests remplacent cette dépendance via
    app.dependency_overrides.
    """
    from app.api.dependencies import get_task_service as service_unique

    return service_unique()


@router.post(
    "",
    response_model=TaskOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Ajouter une tâche",
    responses={422: {"description": "Titre vide, trop long ou priorité inconnue"}},
)
def create_task(payload: TaskInput, service=Depends(get_task_service)):
    try:
        return service.create(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
        )
    except TaskError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get(
    "",
    response_model=list[TaskOutput],
    summary="Consulter la liste des tâches",
)
def list_tasks(status: TaskStatus | None = None, service=Depends(get_task_service)):
    """Toutes les tâches, ou seulement celles du statut demandé (todo | done)."""
    return service.list(status)
