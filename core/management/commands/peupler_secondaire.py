from django.core.management.base import BaseCommand
from core.models import Matiere, Topic

class Command(BaseCommand):
    help = 'Peuple les données pour le secondaire (6ème - Terminale)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Peuplement du secondaire en cours...'))

        # Nouvelles matières
        nouvelles_matieres = [
            {'nom': 'anglais', 'description': 'Anglais : Langue et Culture', 'ordre': 10},
            {'nom': 'svt', 'description': 'Sciences de la Vie et de la Terre', 'ordre': 11},
            {'nom': 'sciences_physiques', 'description': 'Sciences Physiques : Physique et Chimie', 'ordre': 12},
            {'nom': 'philosophie', 'description': 'Philosophie : Pensée et Critique', 'ordre': 13},
            {'nom': 'allemand', 'description': 'Allemand', 'ordre': 14},
            {'nom': 'arabe', 'description': 'Arabe', 'ordre': 15},
        ]

        for m_data in nouvelles_matieres:
            Matiere.objects.get_or_create(nom=m_data['nom'], defaults=m_data)

        # Topics 6ème
        topics_6eme = [
            {'matiere': 'expression_orale', 'titre': 'Grammaire : La phrase simple', 'resume': 'Structure de base de la phrase en français.', 'ordre': 1},
            {'matiere': 'mathematiques', 'titre': 'Nombres entiers et décimaux', 'resume': 'Comprendre et manipuler les nombres au collège.', 'ordre': 1},
            {'matiere': 'anglais', 'titre': 'The Alphabet and Greetings', 'resume': 'Apprendre l\'alphabet et les salutations de base.', 'ordre': 1},
            {'matiere': 'svt', 'titre': 'Le corps humain et ses fonctions', 'resume': 'Introduction à l\'organisation du corps humain.', 'ordre': 1},
        ]

        # Topics 3ème
        topics_3eme = [
            {'matiere': 'mathematiques', 'titre': 'Équations du 2nd degré', 'resume': 'Résoudre des équations complexes.', 'ordre': 1},
            {'matiere': 'histoire', 'titre': 'Les Guerres Mondiales', 'resume': 'Étude des conflits mondiaux du XXe siècle.', 'ordre': 1},
            {'matiere': 'geographie', 'titre': 'La Mondialisation', 'resume': 'Les enjeux du commerce et des échanges mondiaux.', 'ordre': 1},
        ]

        # Topics Terminale D
        topics_td = [
            {'matiere': 'philosophie', 'titre': 'La Conscience et l\'Inconscient', 'resume': 'Étude des fondements de l\'esprit humain.', 'ordre': 1},
            {'matiere': 'svt', 'titre': 'Génétique et Évolution', 'resume': "L'hérédité et l'évolution des espèces.", 'ordre': 1},
            {'matiere': 'sciences_physiques', 'titre': 'Mécanique du point', 'resume': 'Étude du mouvement et des forces.', 'ordre': 1},
        ]

        configs = [
            ('6eme', topics_6eme),
            ('3eme', topics_3eme),
            ('t_d', topics_td),
        ]

        for classe_code, topics in configs:
            self.stdout.write(f'--- Classe {classe_code.upper()} ---')
            for t_data in topics:
                mat = Matiere.objects.get(nom=t_data.pop('matiere'))
                Topic.objects.get_or_create(
                    matiere=mat,
                    classe=classe_code,
                    titre=t_data['titre'],
                    defaults={**t_data, 'matiere': mat}
                )

        self.stdout.write(self.style.SUCCESS('Terminé !'))
