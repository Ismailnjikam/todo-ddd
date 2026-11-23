
/**
 * =====================================================
 * API.JS - Communication avec le backend FastAPI
 * Projet : To-Do List
 * Développeur : Shagui (M11)
 * =====================================================
 */

// Adresse de base du backend FastAPI
const API_BASE_URL = "http://127.0.0.1:8000/tasks";


/**
 * Fonction générique pour effectuer les requêtes HTTP
 */
async function request(endpoint, options = {}) {

    try {

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...options.headers
            }
        });

        // Gestion des réponses sans contenu
        if (response.status === 204) {
            return null;
        }

        // Vérifier le type de contenu de la réponse
        const contentType = response.headers.get("content-type");

        const data = contentType && contentType.includes("application/json")
            ? await response.json()
            : null;

        // Gestion des erreurs HTTP
        if (!response.ok) {
            throw new Error(
                data?.detail || `Erreur HTTP : ${response.status}`
            );
        }

        return data;

    } catch (error) {

        console.error("Erreur API :", error);
        throw error;

    }

}


/**
 * 1. Créer une nouvelle tâche
 * Méthode HTTP : POST
 */
async function createTask(taskData) {
    return await request("", {
        method: "POST",
        body: JSON.stringify(taskData)
    });
}


/**
 * 2. Modifier une tâche existante
 * Méthode HTTP : PUT
 */
async function updateTask(taskId, taskData) {
    return await request(`/${taskId}`, {
        method: "PUT",
        body: JSON.stringify(taskData)
    });
}


/**
 * 3. Terminer une tâche
 * Méthode HTTP : PATCH
 */
async function completeTask(taskId) {
    return await request(`/${taskId}/done`, {
        method: "PATCH"
    });
}


/**
 * 4. Supprimer une tâche
 * Méthode HTTP : DELETE
 */
async function deleteTask(taskId) {
    return await request(`/${taskId}`, {
        method: "DELETE"
    });
}


/**
 * 5. Récupérer la liste des tâches
 * Méthode HTTP : GET
 */
async function listTasks(status = null) {

    const query = status
        ? `?status=${encodeURIComponent(status)}`
        : "";

    return await request(query, {
        method: "GET"
    });

}
