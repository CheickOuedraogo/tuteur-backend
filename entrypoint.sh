#!/bin/sh

# Attendre que la base de données soit prête (optionnel, mais recommandé)
# Ici on fait confiance au healthcheck de docker-compose, mais on peut ajouter un wait-for-it si besoin.

echo "🚀 Démarrage du backend Faso Tuteur..."

# Appliquer les migrations de base de données
echo "📦 Application des migrations..."
python manage.py migrate

# Collecter les fichiers statiques
echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Démarrer Gunicorn
echo "🔥 Lancement du serveur Gunicorn..."
exec gunicorn tuteur_intelligent.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --log-level=info
