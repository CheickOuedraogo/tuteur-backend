# Backend - Tuteur Intelligent

API Django REST pour l'application Tuteur Intelligent.

## Installation

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

1. Créer la base de données MySQL
2. Configurer `.env` à la racine du projet
3. Appliquer les migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Utilisation

```bash
# Charger données initiales
python manage.py charger_donnees_initiales

# Générer audio
python manage.py generer_audio --all

# Lancer le serveur
python manage.py runserver
```

Le serveur sera accessible sur `http://localhost:8000`

## API Endpoints

Voir la documentation complète dans le README principal(BACKEND_DOCUMENTATION.md).
