/* ==========================================================
   todo-ddd — Module M12 : Front-end liste / QA  (static/js/list.js)
   Tout est dans une IIFE : aucune variable globale, donc aucun
   conflit avec api.js (M11) ni form.js (M11).
   ========================================================== */
(() => {
"use strict";

/* ---------- Configuration (à adapter facilement) ---------- */
const API_URL = "";                        // "" = même serveur que FastAPI. Ex. : "http://localhost:8000"
const NEW_TASK_URL = "form.html";          // Page du module M11 (création)
const EDIT_TASK_URL = "form.html?id=";     // Page du module M11 (modification) + id

const PRIORITY_LABELS = { low: "Basse", medium: "Moyenne", high: "Élevée" };
const STATUS_LABELS = { todo: "À faire", done: "Terminée" };

/* ---------- Éléments du DOM ---------- */
const $ = (id) => document.getElementById(id);
const els = {
  list: $("task-list"), state: $("state"), search: $("search"),
  statTotal: $("stat-total"), statTodo: $("stat-todo"), statDone: $("stat-done"),
  modal: $("confirm-modal"), modalConfirm: $("modal-confirm"), modalCancel: $("modal-cancel"),
  toasts: $("toasts"), newBtn: $("btn-new-task"),
};

/* ---------- État de l'application ---------- */
// tasks = liste affichée (déjà filtrée par l'API) ; allTasks = toutes les tâches (pour les statistiques)
const state = { tasks: [], allTasks: [], filter: "all", search: "", taskToDelete: null, requestId: 0 };

/* ---------- Adaptation des données de l'API ----------
   Contrat (REPARTITION.md) : Task = id, title, description, priority, status, created_at
   priority : basse | moyenne | élevée      status : todo | done
   Si le backend change, on ne modifie QUE cette partie. */
const PRIORITY_ALIASES = {
  basse: "low", low: "low",
  moyenne: "medium", medium: "medium",
  "élevée": "high", elevee: "high", high: "high",
};

function normalizeTask(raw) {
  const priorityKey = String(raw.priority ?? "").toLowerCase();
  const statusKey = String(raw.status ?? "todo").toLowerCase();
  return {
    id: raw.id,
    title: raw.title ?? "(Sans titre)",
    description: raw.description ?? "",
    priority: PRIORITY_ALIASES[priorityKey] ?? "medium",
    date: raw.created_at ?? null,
    status: statusKey === "done" ? "done" : "todo",
  };
}

/* ---------- Appels API ----------
   À terme, ces 3 fonctions pourront appeler celles de api.js (M11) :
   listTasks(), completeTask(id), deleteTask(id). */
async function apiRequest(path, options = {}) {
  const response = await fetch(API_URL + path, options);
  if (!response.ok) {
    const error = new Error("HTTP " + response.status);
    error.status = response.status;
    throw error;
  }
  return response.status === 204 ? null : response.json().catch(() => null);
}

// US-07 : le filtre est appliqué par l'API → GET /tasks?status=todo|done
const fetchTasks = (status) => apiRequest(status ? `/tasks?status=${status}` : "/tasks");
const markTaskDone = (id) => apiRequest(`/tasks/${id}/done`, { method: "PATCH" });
const removeTask = (id) => apiRequest(`/tasks/${id}`, { method: "DELETE" });

/* ---------- Notifications ---------- */
function toast(message, type = "info") {
  const el = document.createElement("div");
  el.className = `toast toast--${type}`;
  el.textContent = message;
  els.toasts.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

/* ---------- Affichage des états ---------- */
function showState({ icon, title, text, loading = false, retry = false, newTask = false }) {
  els.list.innerHTML = "";
  els.state.hidden = false;
  els.state.innerHTML = "";

  const top = document.createElement("div");
  if (loading) top.className = "spinner";
  else { top.className = "state__icon"; top.textContent = icon; }
  const h = document.createElement("h3"); h.textContent = title;
  const p = document.createElement("p"); p.textContent = text || "";
  els.state.append(top, h, p);

  if (retry) {
    const b = document.createElement("button");
    b.className = "btn btn--primary"; b.textContent = "Réessayer";
    b.addEventListener("click", loadTasks);
    els.state.appendChild(b);
  }
  if (newTask) {
    const a = document.createElement("a");
    a.className = "btn btn--primary"; a.textContent = "+ Créer une tâche"; a.href = NEW_TASK_URL;
    els.state.appendChild(a);
  }
}
const hideState = () => { els.state.hidden = true; };

/* ---------- Statistiques ---------- */
function updateStats() {
  const done = state.allTasks.filter((t) => t.status === "done").length;
  els.statTotal.textContent = state.allTasks.length;
  els.statDone.textContent = done;
  els.statTodo.textContent = state.allTasks.length - done;
}

/* ---------- Recherche (le filtre de statut est fait par l'API) ---------- */
function getVisibleTasks() {
  const q = state.search.trim().toLowerCase();
  if (!q) return state.tasks;
  return state.tasks.filter((t) => t.title.toLowerCase().includes(q) || t.description.toLowerCase().includes(q));
}

/* ---------- Création d'une carte ---------- */
function formatDate(value) {
  if (!value) return "";
  const d = new Date(value);
  return isNaN(d) ? "" : d.toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
}

function createBadge(text, cls) {
  const s = document.createElement("span");
  s.className = `badge ${cls}`; s.textContent = text;
  return s;
}

function createButton(text, cls, onClick) {
  const b = document.createElement("button");
  b.className = `btn btn--sm ${cls}`; b.textContent = text;
  b.addEventListener("click", onClick);
  return b;
}

function createTaskCard(task) {
  const isDone = task.status === "done";
  const card = document.createElement("article");
  card.className = "task-card" + (isDone ? " is-done" : "");

  const top = document.createElement("div");
  top.className = "task-card__top";
  top.append(
    createBadge(PRIORITY_LABELS[task.priority] || task.priority, `badge--${task.priority}`),
    createBadge(STATUS_LABELS[task.status] || task.status, `badge--${task.status}`)
  );

  const title = document.createElement("h3"); title.textContent = task.title;
  card.append(top, title);

  if (task.description) {
    const desc = document.createElement("p");
    desc.className = "task-card__desc"; desc.textContent = task.description;
    card.appendChild(desc);
  }
  const date = formatDate(task.date);
  if (date) {
    const d = document.createElement("p");
    d.className = "task-card__date"; d.textContent = "📅 Créée le " + date;
    card.appendChild(d);
  }

  const actions = document.createElement("div");
  actions.className = "task-card__actions";
  const doneBtn = createButton(isDone ? "Terminée" : "✓ Terminer", "btn--success", () => handleDone(task, doneBtn));
  doneBtn.disabled = isDone;
  // Lien de modification : le formulaire est géré par M11
  const edit = document.createElement("a");
  edit.className = "btn btn--sm btn--ghost"; edit.textContent = "Modifier"; edit.href = EDIT_TASK_URL + task.id;
  const del = createButton("Supprimer", "btn--outline-danger", () => openDeleteModal(task));
  actions.append(doneBtn, edit, del);
  card.appendChild(actions);

  return card;
}

/* ---------- Rendu principal ---------- */
function render() {
  updateStats();
  if (state.allTasks.length === 0) {
    return showState({ icon: "📝", title: "Aucune tâche pour ce filtre", text: "Créez votre première tâche.", newTask: true });
  }
  const visible = getVisibleTasks();
  if (visible.length === 0) {
    return showState({ icon: "🔍", title: "Aucun résultat", text: "Aucune tâche ne correspond à votre recherche ou au filtre choisi." });
  }
  hideState();
  els.list.replaceChildren(...visible.map(createTaskCard));
}

/* ---------- Chargement ---------- */
const toTasks = (data) => (Array.isArray(data) ? data : data?.tasks ?? data?.items ?? []).map(normalizeTask);

// silent = true : pas d'écran de chargement (après terminer / supprimer)
async function loadTasks({ silent = false } = {}) {
  const myRequest = ++state.requestId;          // ignore les réponses périmées (clics rapides sur les filtres)
  if (!silent) showState({ loading: true, title: "Chargement des tâches…" });
  try {
    const status = state.filter === "all" ? null : state.filter;
    // Liste filtrée par l'API ; si un filtre est actif, on charge aussi toutes les tâches pour les statistiques
    const [filtered, all] = await Promise.all([fetchTasks(status), status ? fetchTasks(null) : null]);
    if (myRequest !== state.requestId) return;
    state.tasks = toTasks(filtered);
    state.allTasks = all ? toTasks(all) : state.tasks;
    render();
  } catch (err) {
    if (myRequest !== state.requestId) return;
    state.tasks = [];
    state.allTasks = [];
    updateStats();
    showState({ icon: "⚠️", title: "Connexion impossible", text: "Impossible de joindre l'API. Vérifiez que le serveur FastAPI est lancé.", retry: true });
  }
}

/* ---------- Terminer une tâche ---------- */
async function handleDone(task, button) {
  button.disabled = true;
  try {
    await markTaskDone(task.id);
    await loadTasks({ silent: true });
    toast("Tâche terminée.", "success");
  } catch (err) {
    if (err.status === 409) { await loadTasks({ silent: true }); toast("La tâche est déjà terminée", "info"); }
    else if (err.status === 404) { toast("Tâche introuvable : la liste va être actualisée.", "error"); loadTasks({ silent: true }); }
    else { button.disabled = false; toast("Une erreur est survenue. Réessayez.", "error"); }
  }
}

/* ---------- Supprimer une tâche (avec confirmation) ---------- */
function openDeleteModal(task) {
  state.taskToDelete = task;
  els.modal.showModal();
}

async function confirmDelete() {
  const task = state.taskToDelete;
  els.modal.close();
  if (!task) return;
  try {
    await removeTask(task.id);
    await loadTasks({ silent: true });
    toast("Tâche supprimée", "success");
  } catch (err) {
    if (err.status === 404) { toast("Tâche introuvable : elle a peut-être déjà été supprimée.", "error"); loadTasks({ silent: true }); }
    else toast("Impossible de supprimer la tâche.", "error");
  } finally {
    state.taskToDelete = null;
  }
}

/* ---------- Événements ---------- */
function initEvents() {
  els.newBtn.href = NEW_TASK_URL;

  els.search.addEventListener("input", (e) => { state.search = e.target.value; render(); });

  document.querySelectorAll(".filter").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter").forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      state.filter = btn.dataset.filter;
      loadTasks();                                 // US-07 : nouvel appel GET /tasks?status=...
    });
  });

  els.modalConfirm.addEventListener("click", confirmDelete);
  els.modalCancel.addEventListener("click", () => { els.modal.close(); state.taskToDelete = null; });
}

/* ---------- Démarrage ---------- */
document.addEventListener("DOMContentLoaded", () => { initEvents(); loadTasks(); });

})();