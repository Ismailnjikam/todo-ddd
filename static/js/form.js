
/**
 * =====================================================
 * FORM.JS - Gestion des formulaires des tâches
 * Projet : To-Do List
 * Développeur : Shagui (M11)
 * =====================================================
 */

// Récupération des éléments HTML
const taskForm = document.querySelector("#task-form");
const titleInput = document.querySelector("#title");
const descriptionInput = document.querySelector("#description");
const priorityInput = document.querySelector("#priority");
const formMessage = document.querySelector("#form-message");
const submitButton = document.querySelector("#submit-button");

// Identifiant de la tâche en cours de modification
let editingTaskId = null;


/**
 * Afficher un message à l'utilisateur
 */
function showFormMessage(message, type = "success") {
    if (!formMessage) return;

    formMessage.textContent = message;
    formMessage.className = `form-message ${type}`;
}


/**
 * Réinitialiser le formulaire
 */
function resetTaskForm() {
    if (!taskForm) return;

    taskForm.reset();
    editingTaskId = null;

    if (submitButton) {
        submitButton.textContent = "Créer la tâche";
    }

    if (formMessage) {
        formMessage.textContent = "";
        formMessage.className = "form-message";
    }
}


/**
 * Préparer le formulaire pour modifier une tâche
 */
function prepareTaskEdit(task) {
    if (!taskForm || !task) return;

    editingTaskId = task.id;

    titleInput.value = task.title || "";
    descriptionInput.value = task.description || "";
    priorityInput.value = task.priority || "moyenne";

    if (submitButton) {
        submitButton.textContent = "Modifier la tâche";
    }

    showFormMessage("Modification de la tâche sélectionnée.", "success");
}


/**
 * Charger la tâche à modifier depuis l'API
 */
async function loadTaskForEdit() {

    const params = new URLSearchParams(window.location.search);
    const taskId = params.get("id");

    // Aucun identifiant : il s'agit d'une création
    if (!taskId) return;

    try {

        showFormMessage("Chargement de la tâche...", "success");

        const tasks = await listTasks();

        const task = tasks.find(
            item => String(item.id) === taskId
        );

        if (!task) {
            showFormMessage("Tâche introuvable.", "error");
            return;
        }

        prepareTaskEdit(task);

    } catch (error) {

        showFormMessage(
            error.message || "Impossible de charger la tâche.",
            "error"
        );

    }
}


/**
 * Vérifier les informations du formulaire
 */
function validateTaskForm(title) {

    if (!title.trim()) {
        return "Le titre est obligatoire.";
    }

    if (title.trim().length > 100) {
        return "Le titre ne doit pas dépasser 100 caractères.";
    }

    return null;
}


/**
 * Gérer la soumission du formulaire
 */
if (taskForm) {

    // Charger une tâche si un identifiant est présent
    loadTaskForEdit();

    taskForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const title = titleInput.value.trim();
        const description = descriptionInput.value.trim();
        const priority = priorityInput.value;

        const validationError = validateTaskForm(title);

        if (validationError) {
            showFormMessage(validationError, "error");
            return;
        }

        const taskData = {
            title: title,
            description: description,
            priority: priority
        };

        try {

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = "Enregistrement...";
            }

            if (editingTaskId !== null) {

                await updateTask(editingTaskId, taskData);

                showFormMessage(
                    "La tâche a été modifiée avec succès.",
                    "success"
                );

            } else {

                await createTask(taskData);

                showFormMessage(
                    "La tâche a été créée avec succès.",
                    "success"
                );

            }

            // Retour à la liste après un enregistrement réussi
            setTimeout(() => {
                window.location.href = "index.html";
            }, 1000);

        } catch (error) {

            showFormMessage(
                error.message || "Une erreur est survenue.",
                "error"
            );

            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent =
                    editingTaskId !== null
                        ? "Modifier la tâche"
                        : "Créer la tâche";
            }

        }

    });

}
