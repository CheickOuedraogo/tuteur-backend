"""
Views API FASO Tuteur - Gestion des exercices et soumissions.
"""
import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from core.models import ProfilEleve, Topic, Exercice, Soumission, Progression
from api.serializers import ExerciceSerializer
from api.exceptions import ExerciceInvalideError

logger = logging.getLogger(__name__)


class ExerciceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Gestion des exercices.
    
    Endpoints:
        GET /exercices/ - Liste des exercices filtrés
        GET /exercices/{id}/ - Détail d'un exercice
        POST /exercices/soumettre/ - Soumettre une réponse
    
    Query params:
        - topic: ID du topic
        - difficulte: Niveau de difficulté (1-3)
    """
    queryset = Exercice.objects.all()
    serializer_class = ExerciceSerializer
    pagination_class = None  # Désactiver pagination (listes filtrées)
    
    def get_queryset(self):
        """Filtre les exercices par topic et difficulté."""
        queryset = Exercice.objects.select_related('topic', 'topic__matiere').all()
        topic_id = self.request.query_params.get('topic', None)
        difficulte = self.request.query_params.get('difficulte', None)
        
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        if difficulte:
            queryset = queryset.filter(difficulte=difficulte)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def soumettre(self, request):
        """
        Soumet une réponse à un exercice.
        
        Body:
            - exercice_id (int): ID de l'exercice
            - reponse_index (int): Index de la réponse choisie
            - temps_reponse (int, optionnel): Temps en secondes
            - classe (str, optionnel): Pour utilisateurs anonymes
        
        Returns:
            200: Feedback avec score, explication, etc.
            400: Données invalides
            404: Exercice non trouvé
        """
        exercice_id = request.data.get('exercice_id')
        reponse_index = request.data.get('reponse_index')
        temps_reponse = request.data.get('temps_reponse', None)
        classe = request.data.get('classe', 'cp1')
        
        # Validation des entrées
        if not exercice_id or reponse_index is None:
            raise ExerciceInvalideError("exercice_id et reponse_index requis")
        
        exercice = get_object_or_404(Exercice, id=exercice_id)
        
        # Récupérer ou créer le profil
        profil = self._get_or_create_profil(request, classe)
        
        # Vérifier réponse
        est_correcte = (reponse_index == exercice.correct_index)
        score = exercice.points_recompense if est_correcte else 0
        
        # Générer explication de la réponse
        options = exercice.options_text or exercice.options_images or []
        reponse_choisie = options[reponse_index] if reponse_index < len(options) else "Inconnue"
        reponse_correcte = options[exercice.correct_index] if exercice.correct_index < len(options) else "Inconnue"
        
        if est_correcte:
            explication = f"Excellente réponse ! {reponse_choisie} est bien la bonne réponse. {exercice.feedback_success_text}"
        else:
            explication = f"Ce n'est pas la bonne réponse. Tu as choisi '{reponse_choisie}', mais la bonne réponse était '{reponse_correcte}'. {exercice.feedback_fail_text}"
        
        # Créer soumission
        Soumission.objects.create(
            eleve=profil,
            exercice=exercice,
            reponse_index=reponse_index,
            est_correcte=est_correcte,
            score=score,
            temps_reponse=temps_reponse
        )
        
        # Mettre à jour progression
        points_total, erreurs_consecutives = self._update_progression(
            profil, exercice, est_correcte, score
        )
        
        logger.info(f"Soumission: user={profil.user.username}, exercice={exercice_id}, correct={est_correcte}")
        
        # Préparer réponse avec feedback détaillé
        feedback = {
            'success': est_correcte,
            'score': score,
            'feedback_text': exercice.feedback_success_text if est_correcte else exercice.feedback_fail_text,
            'explication': explication,
            'reponse_correcte': reponse_correcte,
            'reponse_choisie': reponse_choisie,
            'feedback_audio_url': exercice.feedback_success_audio_url if est_correcte else exercice.feedback_fail_audio_url,
            'visuel_desc': 'Étoiles ! Animations joyeuses !' if est_correcte else 'Essaie encore !',
            'points_total': points_total,
            'erreurs_consecutives': erreurs_consecutives
        }
        
        return Response(feedback, status=status.HTTP_200_OK)
    
    def _get_or_create_profil(self, request, classe):
        """Récupère ou crée le profil élève (authentifié ou anonyme)."""
        if request.user.is_authenticated:
            profil, _ = ProfilEleve.objects.get_or_create(
                user=request.user,
                defaults={'classe': classe}
            )
        else:
            # Utilisateur anonyme via session
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            username_anonyme = f'anonyme_{session_key[:8]}'
            user_anonyme, _ = User.objects.get_or_create(
                username=username_anonyme,
                defaults={'is_active': False}
            )
            profil, _ = ProfilEleve.objects.get_or_create(
                user=user_anonyme,
                defaults={'classe': classe}
            )
        return profil
    
    def _update_progression(self, profil, exercice, est_correcte, score):
        """Met à jour la progression de l'élève."""
        progression, _ = Progression.objects.get_or_create(
            eleve=profil,
            topic=exercice.topic
        )
        progression.exercices_total += 1
        
        if est_correcte:
            progression.exercices_reussis += 1
            progression.score_total += score
            progression.erreurs_consecutives = 0
            profil.points += score
            profil.save()
        else:
            progression.erreurs_consecutives += 1
        
        progression.save()
        return profil.points, progression.erreurs_consecutives


class ExerciceAdaptatifViewSet(viewsets.ViewSet):
    """
    Exercices adaptatifs pour un topic.
    
    Endpoints:
        GET /exercices-adaptatifs/{topic_id}/ - Lot de 5 exercices aléatoires
    
    Query params:
        - exclude[]: IDs d'exercices à exclure
    """
    
    @action(detail=False, methods=['get'], url_path='(?P<topic_id>[^/.]+)')
    def exercices_topic(self, request, topic_id=None):
        """
        Retourne un lot de 5 exercices pour un topic.
        Privilégie les exercices non encore réussis.
        
        Returns:
            200: {exercices: [...], has_more: bool, total_in_topic: int}
            404: Topic non trouvé
        """
        topic = get_object_or_404(Topic.objects.select_related('matiere'), id=topic_id)
        
        # Récupérer profil élève
        profil_actuel = self._get_current_profil(request)
        
        # Exercices déjà réussis
        completed_ids = self._get_completed_exercise_ids(profil_actuel, topic)
        
        # Exercices à exclure (passés en param)
        exclus_ids = request.query_params.getlist('exclude[]') + request.query_params.getlist('exclude')
        final_exclude = list(set(
            list(completed_ids) + [int(id) for id in exclus_ids if str(id).isdigit()]
        ))
        
        # Sélectionner 5 exercices aléatoires
        exercices_queryset = Exercice.objects.filter(topic=topic).exclude(id__in=final_exclude)
        
        # Si pas assez d'exercices non réussis, prendre n'importe lesquels
        if exercices_queryset.count() < 5:
            exercices_queryset = Exercice.objects.filter(topic=topic).exclude(
                id__in=[int(id) for id in exclus_ids if str(id).isdigit()]
            )
        
        exercices = list(exercices_queryset.order_by('?')[:5])
        
        # Vérifier s'il en reste d'autres
        remaining_count = Exercice.objects.filter(topic=topic).exclude(
            id__in=final_exclude + [e.id for e in exercices]
        ).count()
        
        serializer = ExerciceSerializer(exercices, many=True)
        return Response({
            'exercices': serializer.data,
            'has_more': remaining_count > 0,
            'total_in_topic': topic.exercices.count()
        })
    
    def _get_current_profil(self, request):
        """Récupère le profil de l'utilisateur actuel."""
        if request.user.is_authenticated:
            try:
                return ProfilEleve.objects.get(user=request.user)
            except ProfilEleve.DoesNotExist:
                return None
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            username_anonyme = f'anonyme_{session_key[:8]}'
            try:
                user_anonyme = User.objects.get(username=username_anonyme)
                return ProfilEleve.objects.get(user=user_anonyme)
            except (User.DoesNotExist, ProfilEleve.DoesNotExist):
                return None
    
    def _get_completed_exercise_ids(self, profil, topic):
        """Retourne les IDs des exercices déjà réussis."""
        if not profil:
            return []
        return list(Soumission.objects.filter(
            eleve=profil,
            exercice__topic=topic,
            est_correcte=True
        ).values_list('exercice_id', flat=True))
