"""
Commande Django pour générer les fichiers audio (gTTS) pour les topics et exercices.
"""
from django.core.management.base import BaseCommand
from core.models import Topic, Exercice
from ia.services import generate_audio


class Command(BaseCommand):
    help = 'Génère les fichiers audio pour les topics et exercices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--topic-id',
            type=int,
            help='Générer audio pour un topic spécifique',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Générer audio pour tous les topics et exercices',
        )

    def handle(self, *args, **options):
        if options['topic_id']:
            topics = Topic.objects.filter(id=options['topic_id'])
        elif options['all']:
            topics = Topic.objects.all()
        else:
            self.stdout.write(self.style.ERROR('Utilisez --topic-id=X ou --all'))
            return
        
        count = 0
        for topic in topics:
            # Générer audio pour le résumé du topic
            if topic.resume:
                audio_url = generate_audio(topic.resume, lang='fr')
                if audio_url:
                    topic.audio_url = audio_url
                    topic.save()
                    count += 1
                    self.stdout.write(f'  ✓ Audio généré pour topic: {topic.titre}')
            
            # Générer audio pour les exercices du topic
            for exercice in topic.exercices.all():
                # Question
                if exercice.question:
                    audio_url = generate_audio(exercice.question, lang='fr')
                    if audio_url:
                        exercice.question_audio_url = audio_url
                        exercice.save()
                        count += 1
                
                # Feedback success
                if exercice.feedback_success_text:
                    audio_url = generate_audio(exercice.feedback_success_text, lang='fr')
                    if audio_url:
                        exercice.feedback_success_audio_url = audio_url
                        exercice.save()
                        count += 1
                
                # Feedback fail
                if exercice.feedback_fail_text:
                    audio_url = generate_audio(exercice.feedback_fail_text, lang='fr')
                    if audio_url:
                        exercice.feedback_fail_audio_url = audio_url
                        exercice.save()
                        count += 1
        
        self.stdout.write(self.style.SUCCESS(f'{count} fichiers audio générés avec succès !'))
