"""
Views API FASO Tuteur - Gestion des profils élèves.
"""
import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from core.models import ProfilEleve
from api.serializers import ProfilEleveSerializer

logger = logging.getLogger(__name__)


class ProfilEleveViewSet(viewsets.ModelViewSet):
    """
    Gestion des profils élèves.
    
    Endpoints:
        GET /profils/ - Liste des profils (admin)
        GET /profils/mon_profil/ - Profil de l'utilisateur connecté
        PATCH /profils/mon_profil/ - Mise à jour du profil
    """
    queryset = ProfilEleve.objects.all()
    serializer_class = ProfilEleveSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Limite la liste aux profils de l'utilisateur connecté."""
        return ProfilEleve.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'patch'])
    def mon_profil(self, request):
        """
        Récupère ou met à jour le profil de l'utilisateur connecté.
        
        GET: Retourne les détails du profil
        PATCH: Met à jour les champs modifiables (classe, photo_profil)
        
        Returns:
            200: Profil retourné/mis à jour
            400: Données invalides
            404: Profil non trouvé
        """
        profil = get_object_or_404(ProfilEleve, user=request.user)
        
        if request.method == 'PATCH':
            serializer = self.get_serializer(profil, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Profil mis à jour: {request.user.username}")
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(profil)
        return Response(serializer.data)
