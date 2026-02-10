"""
Views API FASO Tuteur - Programme scolaire (Matières et Topics).
"""
import logging

from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings

from core.models import Matiere, Topic, ProfilEleve
from core.programme_officiel import get_matieres_pour_classe
from api.serializers import MatiereSerializer, TopicSerializer

logger = logging.getLogger(__name__)


class MatiereViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste des matières disponibles.
    
    Endpoints:
        GET /matieres/ - Liste de toutes les matières
        GET /matieres/{id}/ - Détail d'une matière
    
    Query params:
        - classe: Filtre les matières adaptées à une classe
    """
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    pagination_class = None  # Désactiver pagination (liste courte)

    def get_queryset(self):
        """
        Filtre les matières selon la classe.
        N'affiche que les matières qui :
          1. Ont au moins un topic pour cette classe
          2. Font partie du programme officiel pour cette classe
        """
        classe = self.request.query_params.get('classe')
        
        # Si pas de classe en param, utiliser celle du profil
        if not classe and self.request.user.is_authenticated:
            try:
                classe = self.request.user.profil_eleve.classe
            except ProfilEleve.DoesNotExist:
                pass
        
        queryset = Matiere.objects.all()
        
        if classe:
            classe = classe.lower()
            
            # Double filtrage :
            # 1) Matières qui ont des topics pour cette classe
            from django.db.models import Exists, OuterRef
            queryset = queryset.filter(
                Exists(Topic.objects.filter(matiere=OuterRef('pk'), classe=classe))
            )
            
            # 2) Matières autorisées par le programme officiel
            matieres_autorisees = get_matieres_pour_classe(classe)
            if matieres_autorisees:
                queryset = queryset.filter(nom__in=matieres_autorisees)
            
        return queryset.order_by('ordre')


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste des topics (chapitres) par matière et classe.
    
    Endpoints:
        GET /topics/ - Liste des topics filtrés
        GET /topics/{id}/ - Détail d'un topic
    
    Query params:
        - matiere: Nom de la matière (ex: mathematiques)
        - classe: Code de la classe (ex: cp1)
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    pagination_class = None  # Désactiver pagination (listes filtrées courtes)
    
    def get_queryset(self):
        """Filtre les topics selon matière et classe."""
        queryset = Topic.objects.select_related('matiere').all()
        matiere = self.request.query_params.get('matiere', None)
        classe = self.request.query_params.get('classe', None)
        
        # Si authentifié, utiliser la classe du profil par défaut
        if self.request.user.is_authenticated and self.action == 'list':
            try:
                profil = self.request.user.profil_eleve
                if not classe:
                    classe = profil.classe
            except ProfilEleve.DoesNotExist:
                pass

        if matiere:
            queryset = queryset.filter(matiere__nom=matiere)
        if classe:
            queryset = queryset.filter(classe=classe)
        
        return queryset.order_by('ordre')
