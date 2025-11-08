# Internship Management – SI de gestion des stages

Plateforme Django pour piloter l'ensemble du cycle de vie des stages : campagnes de recrutement, gestion des offres, candidatures, affectations, suivi des livrables, évaluations et reporting analytique. Captures d'écran à venir.

## Sommaire
- [Prérequis](#prérequis)
- [Installation locale (sans Docker)](#installation-locale-sans-docker)
- [Configuration des variables d'environnement](#configuration-des-variables-denvironnement)
- [Migration, superuser et données de démo](#migration-superuser-et-données-de-démo)
- [Lancer le serveur Django (développement)](#lancer-le-serveur-django-développement)
- [Celery & Redis (tâches planifiées)](#celery--redis-tâches-planifiées)
- [Démarrage via Docker (optionnel)](#démarrage-via-docker-optionnel)
- [Structure du projet](#structure-du-projet)
- [Commandes utiles](#commandes-utiles)
- [Dépannage (FAQ courte)](#dépannage-faq-courte)
- [Sécurité & prod](#sécurité--prod)
- [Roadmap / Contribuer](#roadmap--contribuer)
- [Crédits](#crédits)

## Prérequis

- Python 3.11+ et Git installés.
- PostgreSQL 14+ pour la base de données principale.
- Redis (service local ou conteneur) pour Celery.
- (Optionnel) Docker + Docker Compose pour l'orchestration.
- Outils conseillés : Make (si présent sur votre système), Poetry (gestionnaire d'environnement/de dépendances optionnel).

## Installation locale (sans Docker)

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/votre-organisation/internship_mgmt.git
   cd internship_mgmt
   ```
2. Créer et activer l'environnement virtuel :
   - Windows (PowerShell) :
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS/Linux :
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Mettre à jour pip et installer les dépendances :
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
   Alternative Poetry (si utilisé) :
   ```bash
   poetry install && poetry shell
   ```

## Configuration des variables d'environnement

1. Créer un fichier `.env` à la racine du projet en s'inspirant de l'exemple suivant :
   ```dotenv
   DEBUG=true
   SECRET_KEY=change-me
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/internship_db
   REDIS_URL=redis://localhost:6379/0
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=xxxx
   EMAIL_USE_TLS=true
   ```
2. Les variables sont chargées via `config/settings.py` en s'appuyant sur `django-environ` (ou équivalent).
3. Créer la base de données PostgreSQL si nécessaire :
   ```sql
   CREATE DATABASE internship_db;
   CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres';
   GRANT ALL PRIVILEGES ON DATABASE internship_db TO postgres;
   ```

## Migration, superuser et données de démo

```bash
python manage.py migrate
python manage.py createsuperuser
```

Charger des fixtures ou des données de démonstration si disponibles :
```bash
python manage.py loaddata fixtures/*.json
# ou
python manage.py seed_demo_data
```

## Lancer le serveur Django (développement)

```bash
python manage.py runserver
```

Accès :
- Application : http://127.0.0.1:8000/
- Admin : http://127.0.0.1:8000/admin/

## Celery & Redis (tâches planifiées)

1. S'assurer que Redis est lancé en local (service système ou `docker run redis:7`).
2. Démarrer les workers Celery depuis deux terminaux distincts :
   ```bash
   celery -A config worker -l info
   celery -A config beat -l info
   ```
3. Les tâches automatisent notamment les rappels d'échéances, l'envoi d'e-mails (tuteurs/étudiants), les exports périodiques et le nettoyage des données temporaires.

## Démarrage via Docker (optionnel)

Structure attendue du `docker-compose.yml` : services `web`, `db` (PostgreSQL), `redis`, `worker`, `beat` partageant le même réseau.

Commandes principales :
```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Une fois la pile lancée, l'application et l'admin sont accessibles sur http://localhost:8000/.

## Structure du projet

```
.
├─ config/            # settings, urls, wsgi, celery
├─ apps/
│  ├─ accounts/
│  ├─ entreprises/
│  ├─ offres/
│  ├─ candidatures/
│  ├─ affectations/
│  ├─ suivis/
│  ├─ evaluations/
│  └─ reporting/
├─ templates/
├─ static/
├─ fixtures/
├─ requirements.txt / pyproject.toml
└─ README.md
```

## Commandes utiles

- Collecte des fichiers statiques :
  ```bash
  python manage.py collectstatic
  ```
- Tests automatisés :
  ```bash
  pytest -q
  # ou
  python manage.py test
  ```
- Lint & formatage (si configuré) :
  ```bash
  ruff check .
  ruff format .
  ```

## Dépannage (FAQ courte)

- Erreur de compilation `psycopg` → utiliser `psycopg2-binary` en environnement de développement.
- `django.core.exceptions.ImproperlyConfigured` → vérifier le fichier `.env` et les variables chargées.
- Conflits de migrations → recréer la base locale (`dropdb`/`createdb`) ou exécuter `python manage.py makemigrations` puis `python manage.py migrate`.
- Redis non démarré → aucune tâche Celery ne sera traitée.
- Port 8000 déjà utilisé → lancer `python manage.py runserver 0.0.0.0:8001`.

## Sécurité & prod

- Désactiver le mode debug (`DEBUG=false`) et définir `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.
- Déployer derrière Gunicorn/Nginx, stocker les fichiers médias sur S3/MinIO, utiliser un CDN si nécessaire.
- Mettre en place des sauvegardes PostgreSQL régulières et une rotation des logs.
- Ne jamais committer de secrets : utiliser un coffre-fort ou un gestionnaire de secrets.

## Roadmap / Contribuer

- TODO : portail étudiant public, signature électronique des conventions, API mobile (REST/GraphQL), tableaux de bord PowerBI, intégration SSO.
- Contributions : ouvrir une issue décrivant le besoin, créer une branche dédiée (`feature/nom`), proposer une PR respectant les tests et les conventions (lint/format, messages de commit clairs).
- Licence : à préciser (MIT ou licence propriétaire selon le contexte client).

## Crédits

Projet maintenu par l'équipe Internship Management. Basé sur Django et son écosystème (Django REST Framework, Celery, Redis, Jazzmin, Ruff, Pytest). Merci aux contributeurs et à la communauté open source.
