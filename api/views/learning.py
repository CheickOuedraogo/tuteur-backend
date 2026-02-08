"""
Views API FASO Tuteur - Apprentissage (Accueil et Explications).
"""
import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings

from core.models import ProfilEleve, Matiere, Topic
from api.serializers import MatiereSerializer, TopicSerializer
from ia.services import generate_explication_ia

logger = logging.getLogger(__name__)


class AccueilViewSet(viewsets.ViewSet):
    """
    Données de l'accueil par classe.
    
    Endpoints:
        GET /accueil/{classe}/ - Matières et topics populaires pour la classe
    """
    
    @action(detail=False, methods=['get'], url_path='(?P<classe>[^/.]+)')
    def accueil_classe(self, request, classe=None):
        """
        Retourne les données d'accueil pour une classe.
        
        Args:
            classe: Code de la classe (cp1, ce1, 6eme, etc.)
        
        Returns:
            200: {classe, utilise_ia, matieres, topics_populaires}
        """
        classe = classe.lower()
        
        # Vérifier si classe utilise IA
        utilise_ia = classe not in settings.CLASSES_SANS_IA
        
        # Récupérer matières filtrées
        matieres = Matiere.objects.all().order_by('ordre')
        if classe in ['cp1', 'cp2']:
            matieres = matieres.exclude(
                nom__icontains='histoire'
            ).exclude(
                nom__icontains='geographie'
            ).exclude(
                nom__icontains='géographie'
            )
            
        matieres_data = MatiereSerializer(matieres, many=True).data
        
        # Pour CP1/CP2, ajouter topics populaires
        topics_data = []
        if not utilise_ia:
            topics = Topic.objects.filter(classe=classe)[:5]
            topics_data = TopicSerializer(topics, many=True).data
        
        logger.debug(f"Accueil pour classe {classe}: {len(matieres_data)} matières")
        
        return Response({
            'classe': classe,
            'utilise_ia': utilise_ia,
            'matieres': matieres_data,
            'topics_populaires': topics_data
        })


class ExplicationViewSet(viewsets.ViewSet):
    """
    Explications détaillées des topics.
    
    Endpoints:
        GET /explication/{topic_id}/ - Explication d'un topic
    """
    
    @action(detail=False, methods=['get'], url_path='(?P<topic_id>[^/.]+)')
    def explication_topic(self, request, topic_id=None):
        """
        Retourne l'explication d'un topic.
        
        Pour CP1/CP2: utilise contenu pré-stocké.
        Pour >CP2: génère avec IA si nécessaire.
        
        Returns:
            200: {topic_id, titre, explication, audio_url, image_url, utilise_ia}
            404: Topic non trouvé
        """
        topic = get_object_or_404(Topic.objects.select_related('matiere'), id=topic_id)
        
        # Récupérer profil élève si authentifié
        classe = topic.classe
        if request.user.is_authenticated:
            try:
                profil = ProfilEleve.objects.get(user=request.user)
                classe = profil.classe
            except ProfilEleve.DoesNotExist:
                pass
        
        utilise_ia = classe not in settings.CLASSES_SANS_IA
        
        # Récupérer ou générer le contenu
        explication, audio_url = self._get_or_generate_content(topic, classe, utilise_ia)
        
        logger.info(f"Explication topic {topic_id} pour classe {classe}, IA={utilise_ia}")
        
        return Response({
            'topic_id': topic.id,
            'titre': topic.titre,
            'explication': explication,
            'audio_url': audio_url,
            'image_url': topic.image_url,
            'utilise_ia': utilise_ia
        })
    
    def _get_or_generate_content(self, topic, classe, utilise_ia):
        """
        Récupère le contenu existant ou le génère avec IA.
        
        Returns:
            tuple: (explication, audio_url)
        """
        if topic.contenu_cours:
            # Utiliser le contenu déjà généré
            return topic.contenu_cours, topic.audio_url
        
        if utilise_ia:
            # Générer avec IA si manquant
            result = generate_explication_ia(topic, classe)
            explication = result.get('explication', topic.resume)
            audio_url = result.get('audio_url', topic.audio_url)
            
            # Sauvegarder pour plus tard
            topic.contenu_cours = explication
            if audio_url:
                topic.audio_url = audio_url
            topic.save()
            
            logger.info(f"Contenu IA généré et sauvegardé pour topic {topic.id}")
            return explication, audio_url
        
        # Pour CP1/CP2 sans IA générative
        return topic.resume, topic.audio_url
