#!/bin/bash
# Script d'installation des dépendances avec gestion d'erreurs

echo "🔧 Installation des dépendances du backend..."

cd "$(dirname "$0")"

# Activer l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

source venv/bin/activate

# Mettre à jour pip
echo "⬆️  Mise à jour de pip..."
venv/bin/pip install --upgrade pip --quiet

# Essayer d'installer les dépendances
echo "📥 Installation des packages..."
if venv/bin/pip install -r requirements.txt; then
    echo "✅ Dépendances installées avec succès !"
else
    echo "❌ Erreur lors de l'installation."
    echo ""
    echo "💡 Solutions possibles :"
    echo "1. Vérifiez votre connexion internet"
    echo "2. Essayez d'installer les packages un par un :"
    echo "   source venv/bin/activate"
    echo "   pip install Django"
    echo "   pip install djangorestframework"
    echo "   # etc..."
    echo ""
    echo "3. Consultez INSTALL.md pour plus d'options"
    exit 1
fi

echo ""
echo "✨ Installation terminée !"
echo "Pour activer l'environnement : source venv/bin/activate"
