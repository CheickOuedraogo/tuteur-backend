"""
Views API FASO Tuteur - Module d'authentification.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers import UserSignupSerializer, UserSerializer


class SignupView(viewsets.GenericViewSet):
    """Inscription des nouveaux élèves."""
    serializer_class = UserSignupSerializer
    permission_classes = []

    def create(self, request):
        """
        Crée un nouvel utilisateur avec son profil élève.
        
        Body:
            - username (str): Nom d'utilisateur unique
            - password (str): Mot de passe
            - email (str, optionnel): Email
            - classe (str): Classe de l'élève (cp1, cp2, ce1, etc.)
        
        Returns:
            201: Utilisateur créé avec succès
            400: Données invalides
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Utilisateur créé avec succès",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
