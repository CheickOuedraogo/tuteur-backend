"""
Management command pour pré-générer le contenu IA pour tous les topics.
Usage: python manage.py pre_generate_content [--classe=cp1] [--all]
"""
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Topic
from ia.services import generate_explication_ia

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Pré-génère le contenu IA pour les topics sans contenu'

    def add_arguments(self, parser):
        parser.add_argument(
            '--classe',
            type=str,
            help='Classe spécifique (ex: ce1, cm2, 6eme)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Générer pour toutes les classes qui utilisent l\'IA',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limite le nombre de topics à générer (pour tests)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Régénère même si le contenu existe déjà',
        )

    def handle(self, *args, **options):
        classe = options.get('classe')
        all_classes = options.get('all')
        limit = options.get('limit')
        force = options.get('force')

        # Déterminer les classes à traiter
        if all_classes:
            # Toutes les classes sauf CP1 et CP2
            classes_to_process = [
                'ce1', 'ce2', 'cm1', 'cm2',
                '6eme', '5eme', '4eme', '3eme',
                '2nde', '1ere_d', '1ere_c', 't_d', 't_c'
            ]
        elif classe:
            if classe.lower() in settings.CLASSES_SANS_IA:
                self.stdout.write(
                    self.style.WARNING(
                        f"La classe {classe} n'utilise pas l'IA générative."
                    )
                )
                return
            classes_to_process = [classe.lower()]
        else:
            self.stdout.write(
                self.style.ERROR(
                    'Spécifiez --classe=<classe> ou --all'
                )
            )
            return

        total_generated = 0
        total_skipped = 0
        total_errors = 0

        for current_classe in classes_to_process:
            self.stdout.write(
                self.style.HTTP_INFO(
                    f'\n📚 Traitement de la classe: {current_classe.upper()}'
                )
            )

            # Récupérer les topics de cette classe
            if force:
                topics = Topic.objects.filter(classe=current_classe)
            else:
                topics = Topic.objects.filter(
                    classe=current_classe,
                    contenu_cours__isnull=True
                ) | Topic.objects.filter(
                    classe=current_classe,
                    contenu_cours=''
                )

            if limit:
                topics = topics[:limit]

            topic_count = topics.count()
            
            if topic_count == 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ Aucun topic à générer pour {current_classe}'
                    )
                )
                continue

            self.stdout.write(
                f'  → {topic_count} topic(s) à traiter\n'
            )

            # Traiter chaque topic
            for idx, topic in enumerate(topics, 1):
                try:
                    self.stdout.write(
                        f'  [{idx}/{topic_count}] {topic.titre[:50]}... ',
                        ending=''
                    )

                    # Générer le contenu IA
                    result = generate_explication_ia(topic, current_classe)
                    
                    # Sauvegarder
                    topic.contenu_cours = result.get('explication', topic.resume)
                    if result.get('audio_url'):
                        topic.audio_url = result['audio_url']
                    topic.save()

                    self.stdout.write(
                        self.style.SUCCESS('✓')
                    )
                    total_generated += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Erreur: {str(e)}')
                    )
                    logger.error(
                        f'Erreur génération topic {topic.id}: {e}',
                        exc_info=True
                    )
                    total_errors += 1

        # Résumé final
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {total_generated} topic(s) générés avec succès'
            )
        )
        if total_skipped > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'⊘ {total_skipped} topic(s) ignorés (déjà générés)'
                )
            )
        if total_errors > 0:
            self.stdout.write(
                self.style.ERROR(
                    f'✗ {total_errors} erreur(s) rencontrées'
                )
            )
        self.stdout.write('='*60 + '\n')
