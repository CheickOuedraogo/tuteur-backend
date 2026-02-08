#!/bin/bash
# Script d'initialisation du projet Tuteur Intelligent

echo "🚀 Initialisation du projet Tuteur Intelligent..."

# Activer l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

echo "📥 Installation des dépendances..."
pip install -r requirements.txt

echo "🗄️  Application des migrations..."
python manage.py makemigrations
python manage.py migrate

echo "👤 Création du superutilisateur (optionnel)..."
echo "Appuyez sur Entrée pour ignorer ou créez votre compte admin"
python manage.py createsuperuser || echo "Superutilisateur ignoré"

echo "📚 Chargement des données initiales..."
python manage.py charger_donnees_initiales

echo "🎵 Génération des fichiers audio (peut prendre du temps)..."
read -p "Voulez-vous générer les fichiers audio maintenant ? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    python manage.py generer_audio --all
fi

echo "✅ Projet initialisé avec succès !"
echo "🚀 Pour lancer le serveur : python manage.py runserver"
