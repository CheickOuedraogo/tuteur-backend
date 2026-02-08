"""
API Views - FASO Tuteur

Ce module exporte toutes les vues de l'API de manière centralisée.
La structure modulaire facilite la maintenance et la lisibilité.

Modules:
    - auth: Inscription (SignupView)
    - profile: Gestion des profils élèves (ProfilEleveViewSet)
    - curriculum: Programme scolaire (MatiereViewSet, TopicViewSet)
    - exercises: Exercices et soumissions (ExerciceViewSet, ExerciceAdaptatifViewSet)
    - learning: Apprentissage (AccueilViewSet, ExplicationViewSet)
    - chatbot: Tuteur intelligent Sandy (ChatbotViewSet)
    - progression: Suivi de progression (ProgressionViewSet)
"""

# Auth
from api.views.auth import SignupView

# Profile
from api.views.profile import ProfilEleveViewSet

# Curriculum
from api.views.curriculum import MatiereViewSet, TopicViewSet

# Exercises
from api.views.exercises import ExerciceViewSet, ExerciceAdaptatifViewSet

# Learning
from api.views.learning import AccueilViewSet, ExplicationViewSet

# Chatbot
from api.views.chatbot import ChatbotViewSet

# Progression
from api.views.progression import ProgressionViewSet

# Exports publics
__all__ = [
    'SignupView',
    'ProfilEleveViewSet',
    'MatiereViewSet',
    'TopicViewSet',
    'ExerciceViewSet',
    'ExerciceAdaptatifViewSet',
    'AccueilViewSet',
    'ExplicationViewSet',
    'ChatbotViewSet',
    'ProgressionViewSet',
]
