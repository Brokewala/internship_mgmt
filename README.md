# Internship Management

Plateforme Django 5 pour gérer les entreprises, offres de stage, candidatures et suivis des étudiants. Le projet est préparé pour fonctionner avec PostgreSQL, Redis et Celery, et propose une interface d'administration personnalisée grâce à Jazzmin.

## Fonctionnalités principales

- **Gestion des comptes** avec un modèle utilisateur personnalisé, profils et rôles (administrateur, personnel, tuteur, étudiant).
- **Applications métiers** distinctes : entreprises, offres, candidatures, affectations, suivis, évaluations et reporting.
- **Tableau de bord d'administration** personnalisé avec KPI (Jazzmin).
- **API prête** avec `djangorestframework` et filtres via `django-filter`.
- **Tâches asynchrones** prêtes à l'emploi via Celery + Redis (worker & beat).
- **Commande de peuplement** `seed_demo_data` pour générer un jeu de données de démonstration.

## Prérequis

- Docker & Docker Compose
- GNU Make

## Configuration initiale

1. Copier le fichier d'environnement et l'ajuster si besoin :
   ```bash
   cp .env.example .env
   ```
2. Construire les images et lancer la stack :
   ```bash
   make build
   make up
   ```
3. Appliquer les migrations :
   ```bash
   make migrate
   ```
4. Créer un super utilisateur :
   ```bash
   make createsuperuser
   ```
5. (Optionnel) Générer des données de démonstration :
   ```bash
   make seed
   ```

L'interface Django est disponible sur http://localhost:8000 et l'administration sur http://localhost:8000/admin.

## Services Docker

| Service   | Description                          |
|-----------|--------------------------------------|
| `db`      | Base PostgreSQL 16                    |
| `redis`   | Broker/Backend Redis 7 pour Celery    |
| `web`     | Application Django (gunicorn)        |
| `worker`  | Worker Celery                         |
| `beat`    | Planificateur Celery Beat             |

## Gestion des tâches Celery

Les tâches peuvent être définies dans n'importe quelle application Django via un fichier `tasks.py`. Elles seront automatiquement découvertes grâce à la configuration dans `config/celery.py`.

## Tests & qualité

Les dépendances incluent `Faker` pour la génération de données ainsi que `django-import-export` pour faciliter l'import/export dans l'admin.

## Licence

Projet fourni à titre de squelette pour démarrages rapides.

