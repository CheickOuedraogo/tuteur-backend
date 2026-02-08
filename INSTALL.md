# Guide d'Installation Backend

## Problème de connexion réseau

Si vous rencontrez des erreurs de connexion lors de l'installation des dépendances, voici plusieurs solutions :

### Solution 1 : Vérifier la connexion internet

```bash
ping pypi.org
```

### Solution 2 : Installer les dépendances une par une

```bash
cd backend
source venv/bin/activate

pip install Django
pip install djangorestframework
pip install python-dotenv
pip install gTTS
pip install groq
pip install Pillow
pip install django-cors-headers
pip install boto3

# Pour mysqlclient, vous pourriez avoir besoin de :
# sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

### Solution 3 : Utiliser un proxy ou miroir PyPI

Si vous êtes derrière un proxy ou dans un environnement restreint :

```bash
pip install --proxy http://proxy:port -r requirements.txt
```

Ou utiliser un miroir :
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### Solution 4 : Installation manuelle depuis les wheels

Téléchargez les packages depuis PyPI et installez-les localement :

```bash
pip download -d packages -r requirements.txt
pip install --no-index --find-links packages -r requirements.txt
```

## Après l'installation

Une fois les dépendances installées :

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Charger les données initiales
python manage.py charger_donnees_initiales

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

## Vérification

Pour vérifier que tout est installé correctement :

```bash
python manage.py check
```
