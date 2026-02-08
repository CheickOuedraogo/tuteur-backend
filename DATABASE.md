# Configuration de la Base de Données

## SQLite (Par défaut - Développement)

Le projet utilise maintenant **SQLite** par défaut pour simplifier le développement. Aucune configuration supplémentaire n'est nécessaire.

La base de données sera créée automatiquement dans `backend/db.sqlite3` lors de la première migration.

### Avantages SQLite
- ✅ Aucune installation requise (intégré à Python)
- ✅ Configuration simple
- ✅ Parfait pour le développement
- ✅ Fichier unique facile à sauvegarder

### Commandes

```bash
cd backend
source venv/bin/activate

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Charger les données initiales
python manage.py charger_donnees_initiales
```

## MySQL (Optionnel - Production)

Si vous souhaitez utiliser MySQL en production, décommentez la configuration MySQL dans `tuteur_intelligent/settings.py` et commentez la configuration SQLite.

### Prérequis MySQL
```bash
# Installer mysqlclient
pip install mysqlclient

# Ou sur Ubuntu/Debian
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

### Configuration
1. Créer la base de données MySQL :
```sql
CREATE DATABASE tuteur_intelligent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Configurer `.env` avec vos identifiants MySQL

3. Décommenter la configuration MySQL dans `settings.py`
