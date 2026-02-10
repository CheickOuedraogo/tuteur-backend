# Documentation Technique Backend - FASO Tuteur

Documentation complète du backend Django pour l'application FASO Tuteur, une plateforme éducative pour les élèves du Burkina Faso.

---

## Table des Matières

1. [Architecture du Projet](#architecture-du-projet)
2. [Configuration et Environnement](#configuration-et-environnement)
3. [Modèles de Données](#modèles-de-données)
4. [API REST](#api-rest)
5. [Services IA](#services-ia)
6. [Gestion des Erreurs](#gestion-des-erreurs)
7. [Logging](#logging)
8. [Tests](#tests)
9. [Déploiement en Production](#déploiement-en-production)
10. [Commandes de Management](#commandes-de-management)

---

## Architecture du Projet

```
backend/
├── api/                        # Application API REST
│   ├── views/                  # Vues modulaires
│   │   ├── __init__.py         # Exports publics
│   │   ├── auth.py             # Inscription
│   │   ├── profile.py          # Profils élèves
│   │   ├── curriculum.py       # Matières et Topics
│   │   ├── exercises.py        # Exercices et soumissions
│   │   ├── learning.py         # Accueil et explications
│   │   ├── chatbot.py          # Tuteur Prof. Plankton
│   │   └── progression.py      # Suivi progression
│   ├── exceptions.py           # Exceptions personnalisées
│   ├── serializers.py          # Sérialiseurs DRF
│   ├── urls.py                 # Routes API
│   └── tests.py                # Tests API
├── core/                       # Application métier
│   ├── models.py               # Modèles de données
│   ├── admin.py                # Interface admin
│   ├── management/commands/    # Commandes personnalisées
│   └── tests.py                # Tests modèles
├── ia/                         # Services Intelligence Artificielle
│   ├── services.py             # Groq API, gTTS
│   └── tests.py                # Tests IA
├── tuteur_intelligent/         # Configuration Django
│   ├── settings.py             # Paramètres
│   ├── urls.py                 # Routes principales
│   └── wsgi.py                 # Point d'entrée WSGI
├── logs/                       # Fichiers de logs
├── media/                      # Fichiers uploadés
│   └── audio/                  # Audios générés
├── .env                        # Variables d'environnement
├── requirements.txt            # Dépendances Python
└── manage.py                   # Script Django
```

---

## Configuration et Environnement

### Variables d'Environnement (`.env`)

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `SECRET_KEY` | Clé secrète Django | (obligatoire en prod) |
| `DEBUG` | Mode debug | `True` |
| `ALLOWED_HOSTS` | Hôtes autorisés | `localhost,127.0.0.1` |
| `DATABASE_URL` | Connexion MySQL | `mysql://user:pass@host:port/db` |
| `GROQ_API_KEY` | Clé API Groq (IA) | (obligatoire) |
| `GROQ_MODEL` | Modèle IA | `llama-3.1-8b-instant` |
| `CORS_ALLOWED_ORIGINS` | Origines CORS | `http://localhost:3000,...` |

### Format DATABASE_URL

```
mysql://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

Exemple local:
```
DATABASE_URL=mysql://root:1234@localhost:3306/tuteur
```

---

## Modèles de Données

### ProfilEleve

Profil d'un élève avec sa classe et progression.

| Champ | Type | Description |
|-------|------|-------------|
| `user` | FK → User | Utilisateur Django |
| `classe` | CharField | cp1, cp2, ce1, ..., t_d |
| `photo_profil` | ImageField | Avatar (optionnel) |
| `points` | IntegerField | Points cumulés |
| `badges` | JSONField | Liste de badges |

**Propriétés:**
- `utilise_ia`: Retourne `True` si la classe > CP2

### Matiere

Matière scolaire.

| Champ | Type | Description |
|-------|------|-------------|
| `nom` | CharField | Identifiant (mathematiques, etc.) |
| `description` | TextField | Description |
| `image_url` | URLField | Image d'accueil |
| `ordre` | IntegerField | Ordre d'affichage |

### Topic

Thème/chapitre dans une matière.

| Champ | Type | Description |
|-------|------|-------------|
| `matiere` | FK → Matiere | Matière parente |
| `classe` | CharField | Classe cible |
| `titre` | CharField | Titre du chapitre |
| `resume` | TextField | Résumé court |
| `contenu_cours` | TextField | Contenu détaillé (IA) |
| `audio_url` | URLField | URL audio |

### Exercice

Exercice interactif.

| Champ | Type | Description |
|-------|------|-------------|
| `topic` | FK → Topic | Topic parent |
| `type_exercice` | CharField | choix_multiple, drag_drop, etc. |
| `question` | TextField | Question textuelle |
| `options_text` | JSONField | Options textuelles |
| `correct_index` | IntegerField | Index réponse correcte (0-based) |
| `difficulte` | IntegerField | 1=Facile, 2=Moyen, 3=Difficile |
| `points_recompense` | IntegerField | Points gagnés |

### Soumission

Réponse d'un élève à un exercice.

| Champ | Type | Description |
|-------|------|-------------|
| `eleve` | FK → ProfilEleve | Élève |
| `exercice` | FK → Exercice | Exercice |
| `reponse_index` | IntegerField | Réponse choisie |
| `est_correcte` | BooleanField | Correct ou non |
| `score` | IntegerField | Points obtenus |

### Progression

Suivi de progression par topic.

| Champ | Type | Description |
|-------|------|-------------|
| `eleve` | FK → ProfilEleve | Élève |
| `topic` | FK → Topic | Topic |
| `exercices_reussis` | IntegerField | Nombre de réussites |
| `exercices_total` | IntegerField | Total tentatives |
| `erreurs_consecutives` | IntegerField | Pour adaptation |

---

## API REST

### Endpoints d'Authentification

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/signup/` | Inscription |
| POST | `/api/auth/login/` | Connexion (token) |

### Endpoints Profil

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/profils/mon_profil/` | Récupérer son profil |
| PATCH | `/api/profils/mon_profil/` | Mettre à jour |

### Endpoints Programme

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/matieres/` | Liste des matières |
| GET | `/api/topics/?matiere=X&classe=Y` | Topics filtrés |
| GET | `/api/explication/{topic_id}/` | Contenu détaillé |

### Endpoints Exercices

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/exercices-adaptatifs/{topic_id}/` | 5 exercices aléatoires |
| POST | `/api/exercices/soumettre/` | Soumettre réponse |

### Endpoints Progression

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/progressions/` | Progression par topic |

### Endpoints Chatbot

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/tuteur-intelligent/chat/` | Discuter avec Prof. Plankton |

---

## Services IA

### Configuration

L'IA (Groq) est utilisée uniquement pour les classes > CP2.

```python
# settings.py
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
CLASSES_SANS_IA = ['cp1', 'cp2']
```

### Fonctions Disponibles

| Fonction | Description |
|----------|-------------|
| `call_groq(prompt, classe, contexte)` | Appel API Groq (lève exception si erreur) |
| `call_groq_safe(prompt, ..., default)` | Version sûre avec fallback |
| `generate_audio(text, lang)` | Génération audio gTTS |
| `generate_explication_ia(topic, classe)` | Génère explication + audio |
| `generate_exercice_ia(topic, classe, difficulte)` | Génère un exercice |
| `generate_exercises_batch_ia(topic, classe, count)` | Génère lot d'exercices |
| `chat_tuteur_ia(message, classe, history, user_info)` | Chat avec Prof. Plankton |

---

## Gestion des Erreurs

### Exceptions Personnalisées

Définies dans `api/exceptions.py`:

| Exception | Code HTTP | Cas d'usage |
|-----------|-----------|-------------|
| `FasoTuteurException` | 400 | Base pour toutes les erreurs |
| `IAServiceError` | 503 | Erreur API Groq |
| `IAConfigurationError` | 500 | Clé API manquante |
| `AudioGenerationError` | 500 | Erreur gTTS |
| `ClasseNonAutoriseeError` | 403 | Fonctionnalité non disponible |
| `ExerciceInvalideError` | 400 | Données exercice invalides |

### Format de Réponse Erreur

```json
{
  "success": false,
  "error": {
    "code": "ia_service_error",
    "message": "Le service IA est temporairement indisponible."
  }
}
```

---

## Logging

### Configuration

Les logs sont écrits dans `logs/` avec rotation automatique (5 Mo max, 5 fichiers).

| Fichier | Contenu |
|---------|---------|
| `logs/faso_tuteur.log` | Tous les logs |
| `logs/errors.log` | Erreurs uniquement |

### Utilisation

```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Message de débogage")
logger.info("Information")
logger.warning("Avertissement")
logger.error("Erreur", exc_info=True)
```

---

## Tests

### Exécution

```bash
# Tous les tests
python manage.py test

# Par application
python manage.py test core api ia

# Avec verbosité
python manage.py test --verbosity=2
```

### Structure des Tests

- `core/tests.py`: Modèles (ProfilEleve, Matiere, Topic, etc.)
- `api/tests.py`: Endpoints API (accueil, exercices, explications)
- `ia/tests.py`: Services IA avec mocks

---

## Déploiement en Production

### 1. Configuration Sécurisée

```bash
# .env production
SECRET_KEY=<clé-secrète-générée>
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
DATABASE_URL=mysql://user:password@host:3306/tuteur_prod
GROQ_API_KEY=<votre-clé-groq>
CORS_ALLOWED_ORIGINS=https://votre-domaine.com
```

### 2. Installation des Dépendances

```bash
pip install -r requirements.txt
pip install gunicorn whitenoise
```

### 3. Collecte des Fichiers Statiques

```bash
python manage.py collectstatic --noinput
```

### 4. Migrations Base de Données

```bash
python manage.py migrate
```

### 5. Lancement avec Gunicorn

```bash
gunicorn tuteur_intelligent.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 6. Configuration Nginx (exemple)

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location /static/ {
        alias /chemin/vers/backend/staticfiles/;
    }

    location /media/ {
        alias /chemin/vers/backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Commandes de Management

| Commande | Description |
|----------|-------------|
| `python manage.py charger_donnees_initiales` | Charge les données initiales |
| `python manage.py generer_contenu_cours --classe=cp1` | Génère contenu IA pour les topics |
| `python manage.py generer_exercices --limit=10` | Génère exercices IA |
| `python manage.py generer_audio --audio-only` | Génère audios manquants |
| `python scripts/cleanup_curriculum.py` | Nettoie les doublons et sujets inappropriés |


