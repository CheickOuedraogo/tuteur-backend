"""
Exceptions personnalisées pour l'API FASO Tuteur.
Permet une gestion d'erreurs cohérente et des messages utilisateur clairs.
"""
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)


# === Exceptions Métier ===

class FasoTuteurException(APIException):
    """Exception de base pour toutes les erreurs métier de l'application."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Une erreur est survenue."
    default_code = "error"


class IAServiceError(FasoTuteurException):
    """Erreur lors de l'appel à l'API Groq (IA)."""
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Le service IA est temporairement indisponible. Réessayez plus tard."
    default_code = "ia_service_error"


class IAConfigurationError(FasoTuteurException):
    """Erreur de configuration de l'API IA (clé manquante, etc.)."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Service IA non configuré."
    default_code = "ia_config_error"


class AudioGenerationError(FasoTuteurException):
    """Erreur lors de la génération audio avec gTTS."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Impossible de générer l'audio. Réessayez plus tard."
    default_code = "audio_generation_error"


class ClasseNonAutoriseeError(FasoTuteurException):
    """L'élève n'a pas accès à cette fonctionnalité pour sa classe."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Cette fonctionnalité n'est pas disponible pour votre classe."
    default_code = "classe_non_autorisee"


class ProfilNonTrouveError(FasoTuteurException):
    """Le profil élève n'existe pas."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Profil élève introuvable."
    default_code = "profil_non_trouve"


class ExerciceInvalideError(FasoTuteurException):
    """Données d'exercice invalides."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Données d'exercice invalides."
    default_code = "exercice_invalide"


class ValidationError(FasoTuteurException):
    """Erreur de validation des données entrantes."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Données invalides."
    default_code = "validation_error"


# === Gestionnaire d'erreurs global ===

def custom_exception_handler(exc, context):
    """
    Gestionnaire d'exceptions personnalisé pour DRF.
    - Log toutes les erreurs
    - Formate les réponses de manière cohérente
    """
    # Appeler le handler par défaut de DRF
    response = exception_handler(exc, context)
    
    # Extraire des infos de contexte pour le logging
    view = context.get('view', None)
    request = context.get('request', None)
    
    view_name = getattr(view, '__class__', type(view)).__name__ if view else 'Unknown'
    user = getattr(request, 'user', None)
    user_info = str(user) if user and user.is_authenticated else 'Anonymous'
    
    if response is not None:
        # Log les erreurs 4xx et 5xx
        if response.status_code >= 500:
            logger.error(
                f"[{view_name}] Erreur serveur {response.status_code}: {exc} | User: {user_info}",
                exc_info=True
            )
        elif response.status_code >= 400:
            logger.warning(
                f"[{view_name}] Erreur client {response.status_code}: {exc} | User: {user_info}"
            )
        
        # Formater la réponse de manière cohérente
        response.data = {
            'success': False,
            'error': {
                'code': getattr(exc, 'default_code', 'error'),
                'message': response.data.get('detail', str(exc)) if isinstance(response.data, dict) else str(response.data),
            }
        }
    else:
        # Exception non gérée par DRF
        logger.exception(f"[{view_name}] Exception non gérée: {exc} | User: {user_info}")
    
    return response
