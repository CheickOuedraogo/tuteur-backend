"""
URL Configuration pour l'API FASO Tuteur.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from api.views import (
    SignupView, ProfilEleveViewSet, MatiereViewSet, TopicViewSet,
    ExerciceViewSet, ExerciceAdaptatifViewSet, AccueilViewSet,
    ExplicationViewSet, ChatbotViewSet, ProgressionViewSet
)

router = DefaultRouter()
router.register(r'auth/signup', SignupView, basename='signup')
router.register(r'profils', ProfilEleveViewSet, basename='profil')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'exercices', ExerciceViewSet, basename='exercice')
router.register(r'progressions', ProgressionViewSet, basename='progression')
router.register(r'accueil', AccueilViewSet, basename='accueil')
router.register(r'explication', ExplicationViewSet, basename='explication')
router.register(r'exercices-adaptatifs', ExerciceAdaptatifViewSet, basename='exercice-adaptatif')
router.register(r'tuteur-intelligent', ChatbotViewSet, basename='tuteur-intelligent')

urlpatterns = [
    path('auth/login/', obtain_auth_token),
    path('', include(router.urls)),
]
