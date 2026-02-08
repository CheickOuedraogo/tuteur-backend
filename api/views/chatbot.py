"""
Views API FASO Tuteur - Tuteur Intelligent (Chatbot Sandy).
"""
import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from core.models import ProfilEleve
from api.exceptions import ClasseNonAutoriseeError
from ia.services import chat_tuteur_ia

logger = logging.getLogger(__name__)


class ChatbotViewSet(viewsets.ViewSet):
    """
    Tuteur Intelligent (Chatbot Sandy).
    Disponible pour CE1-Terminale uniquement.
    
    Endpoints:
        POST /tuteur-intelligent/chat/ - Envoyer un message à Sandy
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def chat(self, request):
        """
        Envoie un message au tuteur intelligent Sandy.
        
        Body:
            - message (str): Message de l'élève
            - history (list, optionnel): Historique de conversation
        
        Returns:
            200: {response: str} - Réponse de Sandy
            400: Message requis
            403: Classe non autorisée (CP1/CP2)
            500: Erreur IA
        """
        message = request.data.get('message')
        history = request.data.get('history', [])
        
        if not message:
            return Response(
                {'error': 'Message requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profil = get_object_or_404(ProfilEleve, user=request.user)
        
        # Vérifier si la classe est autorisée (CE1-Terminale)
        if profil.classe in ['cp1', 'cp2']:
            raise ClasseNonAutoriseeError(
                "Le Tuteur Intelligent est disponible à partir du CE1."
            )
        
        user_info = {
            'username': request.user.username,
            'points': profil.points
        }
        
        logger.info(f"Chat Sandy: user={request.user.username}, classe={profil.classe}")
        
        response_text = chat_tuteur_ia(message, profil.classe, history, user_info=user_info)
        
        if not response_text:
            return Response(
                {'error': "Erreur lors de la communication avec l'IA."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        return Response({'response': response_text})
