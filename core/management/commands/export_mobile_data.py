"""
Management command pour exporter les données vers JSON pour l'app mobile.
Usage: python manage.py export_mobile_data
"""
import json
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Matiere, Topic, Exercice

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Exporte les données vers JSON pour l\'application mobile'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='mobile_data.json',
            help='Nom du fichier de sortie',
        )
        parser.add_argument(
            '--classes',
            type=str,
            nargs='+',
            help='Classes spécifiques à exporter (ex: ce1 cm2)',
        )

    def handle(self, *args, **options):
        output_file = options['output']
        classes_filter = options.get('classes')

        self.stdout.write(self.style.HTTP_INFO('📱 Export des données pour mobile...'))

        # Exporter les matières
        matieres = Matiere.objects.all().order_by('ordre')
        matieres_data = []
        
        for matiere in matieres:
            matieres_data.append({
                'id': matiere.id,
                'nom': matiere.nom,
                'icone': self._get_icon_name(matiere.nom),
                'couleur': self._get_color(matiere.nom),
                'ordre': matiere.ordre,
            })

        # Exporter les topics
        topics_query = Topic.objects.select_related('matiere').all()
        
        if classes_filter:
            topics_query = topics_query.filter(classe__in=classes_filter)
            
        topics_data = []
        
        for topic in topics_query:
            topics_data.append({
                'id': topic.id,
                'matiere_id': topic.matiere.id,
                'classe': topic.classe,
                'titre': topic.titre,
                'resume': topic.resume or '',
                'contenu_cours': topic.contenu_cours or '',
                'ordre': topic.ordre,
            })

        # Exporter les exercices
        exercices_query = Exercice.objects.select_related('topic').all()
        
        if classes_filter:
            exercices_query = exercices_query.filter(topic__classe__in=classes_filter)
            
        exercices_data = []
        
        for exercice in exercices_query:
            # Build options from options_text JSON field
            options_list = exercice.options_text if exercice.options_text else []
            
            exercices_data.append({
                'id': exercice.id,
                'topic_id': exercice.topic.id,
                'enonce': exercice.question,  # Use 'question' field
                'options': options_list,
                'reponse_correcte': exercice.correct_index,  # Already 0-indexed
                'difficulte': exercice.difficulte,
            })

        # Créer l'objet JSON final
        data = {
            'version': '1.0.0',
            'export_date': str(timezone.now()),
            'matieres': matieres_data,
            'topics': topics_data,
            'exercices': exercices_data,
        }

        # Sauvegarder dans le fichier
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Statistiques
        self.stdout.write(self.style.SUCCESS(f'\n✅ Export terminé avec succès !'))
        self.stdout.write(f'  📁 Fichier: {output_file}')
        self.stdout.write(f'  📚 Matières: {len(matieres_data)}')
        self.stdout.write(f'  📖 Topics: {len(topics_data)}')
        self.stdout.write(f'  ✏️  Exercices: {len(exercices_data)}')
        
        # Calculer la taille
        import os
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        self.stdout.write(f'  💾 Taille: {size_mb:.2f} MB\n')

    def _get_icon_name(self, matiere_nom):
        """Retourne le nom d'icône Ionicons."""
        icons = {
            'Mathématiques': 'calculator',
            'Français': 'book',
            'Sciences': 'flask',
            'Histoire': 'time',
            'Géographie': 'map',
            'Anglais': 'language',
        }
        return icons.get(matiere_nom, 'book')

    def _get_color(self, matiere_nom):
        """Retourne la couleur de la matière."""
        colors = {
            'Mathématiques': '#3b82f6',
            'Français': '#ec4899',
            'Sciences': '#10b981',
            'Histoire': '#f59e0b',
            'Géographie': '#8b5cf6',
            'Anglais': '#ef4444',
        }
        return colors.get(matiere_nom, '#6b7280')
