# To-Do List (`todo-ddd`) — Guide Complet du Projet

Bienvenue dans le dépôt **`todo-ddd`** ! Ce projet est une application de gestion de tâches (**To-Do List**) réalisée en équipe selon la méthode agile **Scrum**, organisée avec une architecture en couches inspirée du **Domain-Driven Design (DDD)**, dotée d'une API **FastAPI**, d'une interface web légère et d'un pipeline automatisé (**GitHub Actions**, **Pytest**, **Docker**).

Ce document explique simplement :
1. **À quoi sert le projet** et comment il fonctionne ;
2. **Comment le code est organisé** ;
3. **Comment installer et lancer l'application** chez soi (en local ou avec Docker) ;
4. **Comment lancer les tests** ;
5. **Comment chacun contribue** sur [GitHub](https://github.com/signup) selon son rôle (`M1` à `M14`).

---

## Table des matières

- [1. Présentation du projet](#1-présentation-du-projet)
- [2. Architecture en couches (DDD expliqué simplement)](#2-architecture-en-couches-ddd-expliqué-simplement)
- [3. Structure des dossiers du projet](#3-structure-des-dossiers-du-projet)
- [4. Technologies utilisées](#4-technologies-utilisées)
- [5. Démarrer le projet en local (étape par étape)](#5-démarrer-le-projet-en-local-étape-par-étape)
- [6. Lancer l'application avec Docker](#6-lancer-lapplication-avec-docker)
- [7. Tests et Intégration Continue (CI)](#7-tests-et-intégration-continue-ci)
- [8. Organisation de l'équipe (14 rôles) et documents de référence](#8-organisation-de-léquipe-14-rôles-et-documents-de-référence)
- [9. Règles de travail sur Git et GitHub (très important)](#9-règles-de-travail-sur-git-et-github-très-important)
- [10. Aide rapide et problèmes fréquents](#10-aide-rapide-et-problèmes-fréquents)

---

## 1. Présentation du projet

L'application permet de gérer une liste de tâches quotidiennes :
- créer une nouvelle tâche ;
- consulter et filtrer les tâches existantes ;
- modifier une tâche existante ;
- marquer une tâche comme terminée ;
- supprimer une tâche.

Au-delà de la fonctionnalité elle-même, le projet vise à apprendre à **travailler en équipe de manière propre et structurée** : découpage en sprints, définition de règles métier claires, écriture de tests automatisés, relecture de code via Pull Requests et vérification automatique avant toute mise à jour de la branche principale.

---

## 2. Architecture en couches (DDD expliqué simplement)

Plutôt que de tout mélanger dans un seul fichier, le code backend (`app/`) est séparé en **4 couches**. L'idée principale est que **les règles métier (le cœur de l'application) restent indépendantes des outils techniques** (framework web, base de données ou stockage en mémoire, interface).

- **`app/domain/` (Le cœur métier / Domaine)** :
  C'est là que se trouvent les notions métier du projet (par exemple une tâche, son statut, sa priorité) et les règles qui protègent ces données (par exemple empêcher de créer une tâche vide ou gérer le passage à l'état terminé). Cette couche ne doit pas dépendre de FastAPI.
- **`app/application/` (Les cas d'usage / Application)** :
  C'est l'orchestrateur : il enchaîne les actions concrètes de l'application (ex. *créer une tâche*, *lister les tâches*, *marquer une tâche comme terminée*) en s'appuyant sur le domaine et sur un dépôt (`Repository`) qui gère le stockage.
- **`app/api/` (L'API web / Interface HTTP)** :
  C'est la porte d'entrée pour les requêtes HTTP (création, lecture, mise à jour, suppression). Elle utilise **FastAPI** pour les routes et **Pydantic** pour vérifier que les données envoyées ou renvoyées ont le bon format.
- **`app/infrastructure/` (La technique / Infrastructure)** :
  Elle regroupe les composants techniques et l'assemblage des différentes parties de l'application.

À cela s'ajoute **`static/`**, qui contient la partie visible dans le navigateur (page HTML, styles CSS, scripts JavaScript qui appellent l'API).

---

## 3. Structure des dossiers du projet

```text
todo-ddd/
├── .github/
│   ├── ISSUE_TEMPLATE/         # Modèles pour créer des tickets / issues clairs
│   └── workflows/
│       └── ci.yml              # Pipeline automatique : tests pytest + build Docker
├── app/
│   ├── __init__.py
│   ├── domain/                 # Entités, règles métier, événements du domaine
│   ├── application/            # Cas d'usage et dépôt (Repository)
│   ├── infrastructure/         # Adaptateurs et configuration technique
│   └── api/                    # Routes FastAPI et schémas Pydantic
├── docs/
│   ├── REPARTITION.md          # Répartition détaillée des 14 membres (M1 à M14)
│   ├── scrum/                  # Suivi Scrum (backlog, sprints, réunions)
│   ├── ddd/                    # Glossaire métier, schémas et décisions DDD
│   ├── ux/                     # Maquettes / wireframes et critères d'interface
│   └── preuves/                # Captures, logs et preuves de validation
├── static/
│   ├── css/                    # Feuilles de style
│   └── js/                     # Scripts d'interaction avec l'API
├── tests/
│   ├── __init__.py
│   └── test_smoke.py           # Tests automatisés (pytest)
├── Dockerfile                  # Instructions pour construire l'image Docker
├── pytest.ini                  # Configuration de pytest
├── requirements.txt            # Liste des bibliothèques Python nécessaires
└── README.md                   # Ce guide
