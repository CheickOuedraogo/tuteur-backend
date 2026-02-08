# Utiliser une image Python légère officielle
FROM python:3.11-slim

# Définir des variables d'environnement
# Évite que Python n'écrive des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# La sortie de Python est envoyée directement au terminal sans être mise en mémoire tampon
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système requises pour mysqlclient
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-libmysqlclient-dev \
        build-essential \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le reste du code source
COPY . /app/

# Collecter les fichiers statiques (optionnel ici si géré par un volume ou S3, mais utile pour une image autonome)
# RUN python manage.py collectstatic --noinput

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8000

# Commande par défaut pour lancer l'application avec Gunicorn
CMD ["gunicorn", "tuteur_intelligent.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
