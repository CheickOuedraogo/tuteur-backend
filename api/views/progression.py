"""
Views API FASO Tuteur - Progression des élèves.
"""
import logging

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from core.models import ProfilEleve, Progression
from api.serializers import ProgressionSerializer

logger = logging.getLogger(__name__)


class ProgressionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Progression des élèves par topic.
    
    Endpoints:
        GET /progressions/ - Liste des progressions de l'élève connecté
        GET /progressions/{id}/ - Détail d'une progression
    """
    queryset = Progression.objects.all()
    serializer_class = ProgressionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Désactiver pagination (liste par élève)
    
    def get_queryset(self):
        """Retourne uniquement les progressions de l'utilisateur connecté."""
        profil = get_object_or_404(ProfilEleve, user=self.request.user)
        return Progression.objects.filter(
            eleve=profil
        ).select_related('topic', 'topic__matiere')
