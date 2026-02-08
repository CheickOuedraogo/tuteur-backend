"""
Commande Django pour générer le contenu détaillé des cours avec l'IA (Groq).
Améliorée pour gérer le volume et les erreurs.
"""
import time
import logging
from django.core.management.base import BaseCommand
from django.db.models import Q
from core.models import Topic
from ia.services import generate_explication_ia

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Génère le contenu et l\'audio des cours manquants via IA de manière robuste'

    def add_arguments(self, parser):
        parser.add_argument('--classe', type=str, help='Filtrer par classe (cp1, cp2, etc.)')
        parser.add_argument('--audio-only', action='store_true', help='Générer seulement les audios manquants')
        parser.add_argument('--limit', type=int, default=50, help='Nombre maximum de topics à traiter')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Démarrage de la génération robuste ---'))
        
        classe = options.get('classe')
        audio_only = options.get('audio_only')
        limit = options.get('limit')
        
        # Filtre de base
        query = Q()
        if classe:
            query &= Q(classe=classe)
            
        if audio_only:
            query &= (Q(audio_url__isnull=True) | Q(audio_url=''))
        else:
            query &= (
                Q(contenu_cours__isnull=True) | 
                Q(contenu_cours='') | 
                Q(audio_url__isnull=True) | 
                Q(audio_url='')
            )
        
        topics = Topic.objects.filter(query).order_by('classe', 'ordre')[:limit]
        total = topics.count()
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS('Aucun topic ne nécessite de mise à jour !'))
            return

        self.stdout.write(f'Topics à traiter (limite {limit}) : {total}')
        
        count_success = 0
        count_error = 0
        
        for index, topic in enumerate(topics):
            self.stdout.write(f'[{index+1}/{total}] {topic.classe.upper()} - {topic.titre}...')
            
            try:
                # Si on a déjà le contenu mais qu'on veut l'audio
                if audio_only or (topic.contenu_cours and not topic.audio_url):
                    from ia.services import generate_audio
                    self.stdout.write(f'  -> Génération audio uniquement...')
                    audio_url = generate_audio(topic.contenu_cours)
                    if audio_url:
                        topic.audio_url = audio_url
                        topic.save()
                        count_success += 1
                        self.stdout.write(self.style.SUCCESS(f'    ✓ Audio OK'))
                    else:
                        self.stdout.write(self.style.ERROR(f'    ✗ Échec audio'))
                        count_error += 1
                else:
                    # Génération complète (contenu + audio)
                    result = generate_explication_ia(topic, topic.classe, generate_audio_flag=True)
                    
                    if result and result.get('explication'):
                        topic.contenu_cours = result['explication']
                        if result.get('audio_url'):
                            topic.audio_url = result['audio_url']
                        
                        topic.save()
                        count_success += 1
                        self.stdout.write(self.style.SUCCESS(f'    ✓ Contenu et Audio OK'))
                    else:
                        self.stdout.write(self.style.WARNING(f'    ! IA vide, fallback résumé'))
                        topic.contenu_cours = topic.resume
                        topic.save()
                        count_success += 1
                
                # Pause pour éviter le Rate Limit
                time.sleep(2)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'    ✗ Erreur: {e}'))
                count_error += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nTerminé ! Succès: {count_success}, Erreurs: {count_error}'))
