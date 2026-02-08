"""
Commande Django pour charger les données initiales (matières, topics, exercices)
basées sur le programme scolaire OFFICIEL et COMPLET du Burkina Faso (CP1 à CM2).
"""
from django.core.management.base import BaseCommand
from core.models import Matiere, Topic, Exercice


class Command(BaseCommand):
    help = 'Charge les données initiales du programme scolaire complet (CP1-CM2)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Chargement des données initiales...'))
        
        # Créer matières
        matieres_data = [
            {'nom': 'expression_orale', 'description': 'Expression Orale : Lecture, Écriture, Grammaire, Conjugaison, Vocabulaire', 'ordre': 1},
            {'nom': 'mathematiques', 'description': 'Mathématiques : Numération, Opérations, Géométrie, Mesures, Problèmes', 'ordre': 2},
            {'nom': 'sciences', 'description': 'Sciences d\'Observation : Vie, Santé, Environnement, Matière', 'ordre': 3},
            {'nom': 'histoire', 'description': 'Histoire : Temps, Famille, Village, Pays, Afrique, Monde', 'ordre': 4},
            {'nom': 'geographie', 'description': 'Géographie : Espace, Paysages, Régions, Burkina, Monde', 'ordre': 5},
            {'nom': 'ecm', 'description': 'Éducation Civique et Morale : Vivre ensemble, Citoyenneté, Droits', 'ordre': 6},
            {'nom': 'eps', 'description': 'Éducation Physique et Sportive', 'ordre': 7},
            {'nom': 'arts', 'description': 'Arts et Culture : Dessin, Musique, Artisanat', 'ordre': 8},
            {'nom': 'app', 'description': 'Activités Pratiques de Production', 'ordre': 9},
        ]
        
        for mat_data in matieres_data:
            matiere, created = Matiere.objects.get_or_create(
                nom=mat_data['nom'],
                defaults=mat_data
            )
            if created:
                self.stdout.write(f'  ✓ Matière créée: {matiere.get_nom_display()}')
        
        # --- CP1 ---
        topics_cp1 = [
            # Français (Détaillé)
            {'matiere': 'expression_orale', 'titre': 'Préapprentissage : Graphisme', 'resume': 'Tracé de formes, trajectoires, préparation à l\'écriture.', 'ordre': 1},
            {'matiere': 'expression_orale', 'titre': 'Vocabulaire : École et Classe', 'resume': 'Nommer les objets de la classe et de l\'école.', 'ordre': 2},
            {'matiere': 'expression_orale', 'titre': 'Vocabulaire : Famille', 'resume': 'Nommer les membres de la famille (papa, maman, etc.).', 'ordre': 3},
            {'matiere': 'expression_orale', 'titre': 'Vocabulaire : Corps Humain', 'resume': 'Nommer les parties du corps.', 'ordre': 4},
            {'matiere': 'expression_orale', 'titre': 'Lecture : Voyelles (i, u, o, a)', 'resume': 'Reconnaissance et écriture des voyelles.', 'ordre': 5},
            {'matiere': 'expression_orale', 'titre': 'Lecture : Consonnes et Syllabes', 'resume': 'Formation de syllabes simples (pa, to, mi...).', 'ordre': 6},
            {'matiere': 'expression_orale', 'titre': 'Lecture : Mots et Phrases', 'resume': 'Lecture de mots courants et petites phrases.', 'ordre': 7},
            
            # Maths
            {'matiere': 'mathematiques', 'titre': 'Numération 0-10', 'resume': 'Compter et écrire jusqu\'à 10.', 'ordre': 1},
            {'matiere': 'mathematiques', 'titre': 'Numération 11-20', 'resume': 'Compter et écrire jusqu\'à 20.', 'ordre': 2},
            {'matiere': 'mathematiques', 'titre': 'Addition (sans retenue)', 'resume': 'Introduction au sens de l\'addition.', 'ordre': 3},
            {'matiere': 'mathematiques', 'titre': 'Soustraction (sans retenue)', 'resume': 'Introduction au sens de la soustraction.', 'ordre': 4},
            {'matiere': 'mathematiques', 'titre': 'Géométrie : Algorithmes', 'resume': 'Suites logiques de formes et couleurs.', 'ordre': 5},
            {'matiere': 'mathematiques', 'titre': 'Géométrie : Formes Simples', 'resume': 'Carré, triangle, cercle, rectangle.', 'ordre': 6},
            {'matiere': 'mathematiques', 'titre': 'Mesures : Longueur', 'resume': 'Comparer des longueurs (plus long, plus court).', 'ordre': 7},
            {'matiere': 'mathematiques', 'titre': 'Monnaie', 'resume': 'Pièces de 1, 5, 10, 25, 50, 100 FCFA.', 'ordre': 8},

            # Sciences
            {'matiere': 'sciences', 'titre': 'Les 5 Sens', 'resume': 'Vue, ouïe, odorat, goût, toucher.', 'ordre': 1},
            {'matiere': 'sciences', 'titre': 'Les Animaux Familiers', 'resume': 'Chien, chat, mouton, poule.', 'ordre': 2},
            {'matiere': 'sciences', 'titre': 'Les Plantes', 'resume': 'Arbres, fleurs, feuilles.', 'ordre': 3},
             {'matiere': 'sciences', 'titre': 'L\'Eau', 'resume': 'Usages de l\'eau (boire, laver).', 'ordre': 4},

            # ECM
            {'matiere': 'ecm', 'titre': 'Hygiène Corporelle', 'resume': 'Se laver, se brosser les dents.', 'ordre': 1},
            {'matiere': 'ecm', 'titre': 'Politesse et Respect', 'resume': 'Saluer, remercier.', 'ordre': 2},
            {'matiere': 'ecm', 'titre': 'Symboles Nationaux (Intro)', 'resume': 'Drapeau du Burkina Faso.', 'ordre': 3},
        ]

        # --- CP2 ---
        topics_cp2 = [
            # Français
            {'matiere': 'expression_orale', 'titre': 'Lecture : Sons Complexes', 'resume': 'ou, an, on, in, oi, ai, ei...', 'ordre': 1},
             {'matiere': 'expression_orale', 'titre': 'Grammaire : Le Nom', 'resume': 'Identifier les noms (personne, animal, chose).', 'ordre': 2},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Le Genre', 'resume': 'Masculin et Féminin (un/une, le/la).', 'ordre': 3},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Le Nombre', 'resume': 'Singulier et Pluriel (le/les).', 'ordre': 4},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Le Verbe', 'resume': 'Identifier l\'action dans la phrase.', 'ordre': 5},
            {'matiere': 'expression_orale', 'titre': 'Conjugaison : Présent', 'resume': 'Verbes en -er et être/avoir au présent.', 'ordre': 6},

            # Maths
            {'matiere': 'mathematiques', 'titre': 'Nombres 0-100', 'resume': 'Dizaines et unités.', 'ordre': 1},
            {'matiere': 'mathematiques', 'titre': 'Addition avec Retenue', 'resume': 'Technique de l\'addition posée.', 'ordre': 2},
            {'matiere': 'mathematiques', 'titre': 'Soustraction avec Retenue', 'resume': 'Technique de la soustraction posée.', 'ordre': 3},
            {'matiere': 'mathematiques', 'titre': 'Multiplication : Tables 2,3,4,5', 'resume': 'Mémoriser les tables de multiplication.', 'ordre': 4},
            {'matiere': 'mathematiques', 'titre': 'Géométrie : Droites', 'resume': 'Tracer à la règle.', 'ordre': 5},
             {'matiere': 'mathematiques', 'titre': 'Mesures : Heure', 'resume': 'Lire l\'heure pile et demie.', 'ordre': 6},

            # Histoire/Géo (Début)
            {'matiere': 'histoire', 'titre': 'Le Temps', 'resume': 'Hier, Aujourd\'hui, Demain, Semaine.', 'ordre': 1},
            {'matiere': 'geographie', 'titre': 'Mon Espace', 'resume': 'Ma classe, mon école, le chemin de l\'école.', 'ordre': 1},
        ]

        # --- CE1 ---
        topics_ce1 = [
            # Français
            {'matiere': 'expression_orale', 'titre': 'Lecture : Textes Variés', 'resume': 'Contes, récits, documentaires.', 'ordre': 1},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : La Phrase', 'resume': 'Phrase affirmative, négative, interrogative.', 'ordre': 2},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Sujet et Verbe', 'resume': 'Accord sujet-verbe simple.', 'ordre': 3},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Adjectif Qualificatif', 'resume': 'Reconnaître et accorder l\'adjectif.', 'ordre': 4},
             {'matiere': 'expression_orale', 'titre': 'Conjugaison : Futur Simple', 'resume': 'Verbes du 1er et 2ème groupe.', 'ordre': 5},
            {'matiere': 'expression_orale', 'titre': 'Conjugaison : Passé Composé', 'resume': 'Introduction avec avoir et être.', 'ordre': 6},
            {'matiere': 'expression_orale', 'titre': 'Conjugaison : Imparfait', 'resume': 'Introduction à l\'imparfait.', 'ordre': 7},
            {'matiere': 'expression_orale', 'titre': 'Vocabulaire : Familles de Mots', 'resume': 'Mots de la même famille, préfixes/suffixes.', 'ordre': 8},

            # Maths
            {'matiere': 'mathematiques', 'titre': 'Nombres 0-10 000', 'resume': 'Lecture, écriture, décomposition.', 'ordre': 1},
            {'matiere': 'mathematiques', 'titre': 'Multiplication (Technique)', 'resume': 'Multiplication posée à 1 et 2 chiffres.', 'ordre': 2},
            {'matiere': 'mathematiques', 'titre': 'Division (Partage)', 'resume': 'Notion de partage et division exacte.', 'ordre': 3},
            {'matiere': 'mathematiques', 'titre': 'Géométrie : Angles', 'resume': 'L\'angle droit, l\'équerre.', 'ordre': 4},
            {'matiere': 'mathematiques', 'titre': 'Géométrie : Polygones', 'resume': 'Triangle, quadrilatère, pentagone.', 'ordre': 5},
            {'matiere': 'mathematiques', 'titre': 'Mesures : Masse (kg, g)', 'resume': 'Conversions simples kg <-> g.', 'ordre': 6},

            # Histoire/Géo
            {'matiere': 'histoire', 'titre': 'La Famille et Générations', 'resume': 'Arbre généalogique, ancêtres.', 'ordre': 1},
            {'matiere': 'histoire', 'titre': 'Histoire Locale', 'resume': 'Histoire du village ou du quartier.', 'ordre': 2},
             {'matiere': 'geographie', 'titre': 'Le Plan', 'resume': 'Lire et dessiner un plan simple.', 'ordre': 1},
            {'matiere': 'geographie', 'titre': 'Les Paysages', 'resume': 'Ville, campagne, savane.', 'ordre': 2},
            
             # Sciences
            {'matiere': 'sciences', 'titre': 'L\'Air', 'resume': 'L\'air existe, le vent.', 'ordre': 1},
            {'matiere': 'sciences', 'titre': 'L\'Eau : Cycle', 'resume': 'Évaporation, pluie, ruissellement.', 'ordre': 2},
        ]

        # --- CE2 ---
        topics_ce2 = [
            # Français
            {'matiere': 'expression_orale', 'titre': 'Grammaire : COD / COI', 'resume': 'Compléments d\'objet direct et indirect.', 'ordre': 1},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Compléments Circonstanciels', 'resume': 'Lieu, Temps, Manière.', 'ordre': 2},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Pronoms', 'resume': 'Pronoms personnels sujets et compléments.', 'ordre': 3},
            {'matiere': 'expression_orale', 'titre': 'Conjugaison : Passé Simple', 'resume': 'Introduction (3e personne).', 'ordre': 4},
            {'matiere': 'expression_orale', 'titre': 'Vocabulaire : Sens Propre/Figuré', 'resume': 'Distinguer les deux sens d\'un mot.', 'ordre': 5},

            # Maths
            {'matiere': 'mathematiques', 'titre': 'Nombres 0-100 000', 'resume': 'Grands nombres.', 'ordre': 1},
            {'matiere': 'mathematiques', 'titre': 'Fractions Simples', 'resume': 'Demi, tiers, quart.', 'ordre': 2},
            {'matiere': 'mathematiques', 'titre': 'Division Euclidienne', 'resume': 'Technique opératoire.', 'ordre': 3},
             {'matiere': 'mathematiques', 'titre': 'Géométrie : Cercle', 'resume': 'Rayon, diamètre, compas.', 'ordre': 4},
            {'matiere': 'mathematiques', 'titre': 'Géométrie : Solides', 'resume': 'Cube, pavé droit.', 'ordre': 5},
            {'matiere': 'mathematiques', 'titre': 'Mesures : Périmètre', 'resume': 'Calcul du périmètre carré/rectangle.', 'ordre': 6},

            # Histoire
            {'matiere': 'histoire', 'titre': 'La Préhistoire', 'resume': 'Paléolithique, Néolithique, Feu, Outils.', 'ordre': 1},
            {'matiere': 'histoire', 'titre': 'Les Royaumes Mossi', 'resume': 'Ouédraogo, Oubri, Organisation.', 'ordre': 2},
            {'matiere': 'histoire', 'titre': 'La Colonisation', 'resume': 'Explorateurs, Conquête.', 'ordre': 3},

            # Géo
            {'matiere': 'geographie', 'titre': 'Relief du Burkina', 'resume': 'Plaines, collines, Mont Tenakourou.', 'ordre': 1},
            {'matiere': 'geographie', 'titre': 'Climat et Saisons', 'resume': 'Saison sèche, hivernage.', 'ordre': 2},
             {'matiere': 'geographie', 'titre': 'Cours d\'eau du Burkina', 'resume': 'Les 3 Mouhoun (Volta), Comoé, Niger.', 'ordre': 3},
            {'matiere': 'geographie', 'titre': 'Régions du Burkina', 'resume': 'Découpage administratif.', 'ordre': 4},
        ]

        # --- CM1 ---
        topics_cm1 = [
            # Français
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Phrase Complexe', 'resume': 'Propositions juxtaposées, coordonnées.', 'ordre': 1},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Voix Active/Passive', 'resume': 'Transformation active <-> passive.', 'ordre': 2},
            {'matiere': 'expression_orale', 'titre': 'Conjugaison : Plus-que-parfait', 'resume': 'Formation et emploi.', 'ordre': 3},
             {'matiere': 'expression_orale', 'titre': 'Conjugaison : Conditionnel', 'resume': 'Présent du conditionnel.', 'ordre': 4},
            {'matiere': 'expression_orale', 'titre': 'Orthographe : Participe Passé', 'resume': 'Accords avec être et avoir.', 'ordre': 5},

            # Maths
            {'matiere': 'mathematiques', 'titre': 'Nombres Décimaux', 'resume': 'Virgule, partie entière/décimale.', 'ordre': 1},
             {'matiere': 'mathematiques', 'titre': 'Opérations Décimaux', 'resume': 'Add, Sous, Mult des nombres à virgule.', 'ordre': 2},
            {'matiere': 'mathematiques', 'titre': 'Division Décimale', 'resume': 'Quotient décimal.', 'ordre': 3},
            {'matiere': 'mathematiques', 'titre': 'Aires', 'resume': 'Formules : Carré, Rectangle, Triangle.', 'ordre': 4},
            {'matiere': 'mathematiques', 'titre': 'Volumes', 'resume': 'Formules : Cube, Pavé.', 'ordre': 5},
            {'matiere': 'mathematiques', 'titre': 'Proportionnalité', 'resume': 'Règle de trois, Échelles, Pourcentages.', 'ordre': 6},

            # Sciences
            {'matiere': 'sciences', 'titre': 'Digestion', 'resume': 'Trajet des aliments, hygiène.', 'ordre': 1},
            {'matiere': 'sciences', 'titre': 'Respiration', 'resume': 'Poumons, air inspiré/expiré.', 'ordre': 2},
            {'matiere': 'sciences', 'titre': 'Circulation Sanguine', 'resume': 'Cœur, sang, vaisseaux.', 'ordre': 3},
            {'matiere': 'sciences', 'titre': 'Électricité', 'resume': 'Circuit simple, pile, ampoule.', 'ordre': 4},

            # Histoire
            {'matiere': 'histoire', 'titre': 'Empires Soudanais', 'resume': 'Ghana, Mali, Songhaï.', 'ordre': 1},
            {'matiere': 'histoire', 'titre': 'Royaume de Kong', 'resume': 'Goula.', 'ordre': 2},
            {'matiere': 'histoire', 'titre': 'Résistances Coloniales', 'resume': 'Héros de la résistance.', 'ordre': 3},

            # Géo
            {'matiere': 'geographie', 'titre': 'Population du Burkina', 'resume': 'Ethnies, densité, répartition.', 'ordre': 1},
            {'matiere': 'geographie', 'titre': 'Économie : Agriculture', 'resume': 'Cultures vivrières et de rente.', 'ordre': 2},
            {'matiere': 'geographie', 'titre': 'Économie : Élevage/Mines', 'resume': 'Bétail, Or.', 'ordre': 3},
             {'matiere': 'geographie', 'titre': 'Afrique de l\'Ouest', 'resume': 'Pays, Relief, Climat.', 'ordre': 4},
        ]

        # --- CM2 ---
        topics_cm2 = [
            # Français
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Analyse Logique', 'resume': 'Nature et fonction des propositions.', 'ordre': 1},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Subordonnée Relative', 'resume': 'Pronom relatif, antécédent.', 'ordre': 2},
            {'matiere': 'expression_orale', 'titre': 'Grammaire : Subordonnée Conjonctive', 'resume': 'Complétive, Circonstancielle.', 'ordre': 3},
            {'matiere': 'expression_orale', 'titre': 'Conjugaison : Subjonctif', 'resume': 'Présent du subjonctif.', 'ordre': 4},
             {'matiere': 'expression_orale', 'titre': 'Conjugaison : Concordance', 'resume': 'Harmonie des temps.', 'ordre': 5},

            # Maths
            {'matiere': 'mathematiques', 'titre': 'Grands Nombres (Milliards)', 'resume': 'Jusqu\'aux milliards.', 'ordre': 1},
            {'matiere': 'mathematiques', 'titre': 'Fractions et Décimaux', 'resume': 'Passage de l\'un à l\'autre.', 'ordre': 2},
            {'matiere': 'mathematiques', 'titre': 'Géométrie : Cercle et Disque', 'resume': 'Circonférence, Aire (Pi).', 'ordre': 3},
            {'matiere': 'mathematiques', 'titre': 'Géométrie : Cylindre/Cône', 'resume': 'Volumes complexes.', 'ordre': 4},
            {'matiere': 'mathematiques', 'titre': 'Problèmes Complexes', 'resume': 'Vitesse, Intérêts, Soldes.', 'ordre': 5},

            # Sciences
            {'matiere': 'sciences', 'titre': 'Reproduction Humaine', 'resume': 'Organes, fécondation, grossesse.', 'ordre': 1},
            {'matiere': 'sciences', 'titre': 'Santé de la Reproduction', 'resume': 'Puberté, Hygiène, IST/VIH.', 'ordre': 2},
            {'matiere': 'sciences', 'titre': 'Écosystèmes', 'resume': 'Chaîne alimentaire, équilibre naturel.', 'ordre': 3},
            {'matiere': 'sciences', 'titre': 'Environnement', 'resume': 'Pollution, Réchauffement, Protection.', 'ordre': 4},

            # Histoire
            {'matiere': 'histoire', 'titre': 'Indépendance (1960)', 'resume': 'Processus, Maurice Yaméogo.', 'ordre': 1},
            {'matiere': 'histoire', 'titre': 'Haute-Volta au Burkina Faso', 'resume': 'Révolution de 1983, Thomas Sankara.', 'ordre': 2},
            {'matiere': 'histoire', 'titre': 'Le Burkina Actuel', 'resume': 'Démocratie, Constitution.', 'ordre': 3},
            {'matiere': 'histoire', 'titre': 'L\'Afrique', 'resume': 'Colonisation, Indépendances, OUA/UA.', 'ordre': 4},
            {'matiere': 'histoire', 'titre': 'Le Monde Contemporain', 'resume': 'ONU, Grandes Puissances.', 'ordre': 5},

            # Géo
            {'matiere': 'geographie', 'titre': 'L\'Afrique (Physique/Pol)', 'resume': 'Carte d\'Afrique, Climat, Pays.', 'ordre': 1},
            {'matiere': 'geographie', 'titre': 'Le Monde : Continents', 'resume': 'Europe, Asie, Amérique, Océanie.', 'ordre': 2},
            {'matiere': 'geographie', 'titre': 'Mondialisation', 'resume': 'Commerce mondial, Internet.', 'ordre': 3},
            
            # ECM (CM2 Spécifique)
            {'matiere': 'ecm', 'titre': 'La Constitution', 'resume': 'Loi fondamentale.', 'ordre': 1},
            {'matiere': 'ecm', 'titre': 'Droits de l\'Homme/Enfant', 'resume': 'CDE, DUDH.', 'ordre': 2},
            {'matiere': 'ecm', 'titre': 'Citoyenneté', 'resume': 'Vote, Impôt, Devoirs.', 'ordre': 3},
        ]

        CLASSES_CONFIG = [
            ('cp1', topics_cp1),
            ('cp2', topics_cp2),
            ('ce1', topics_ce1),
            ('ce2', topics_ce2),
            ('cm1', topics_cm1),
            ('cm2', topics_cm2),
        ]

        for classe_code, topics_list in CLASSES_CONFIG:
            self.stdout.write(f'--- Traitement Classe {classe_code.upper()} ---')
            for topic_data in topics_list:
                matiere_nom = topic_data.pop('matiere')
                try:
                    matiere = Matiere.objects.get(nom=matiere_nom)
                    topic, created = Topic.objects.get_or_create(
                        matiere=matiere,
                        classe=classe_code,
                        titre=topic_data['titre'],
                        defaults={
                            **topic_data,
                            'matiere': matiere
                        }
                    )
                    if created:
                        self.stdout.write(f'  ✓ Topic {classe_code.upper()} créé: {topic.titre}')
                    else:
                         # Update resume if exists
                        topic.resume = topic_data['resume']
                        topic.ordre = topic_data['ordre']
                        topic.save()
                except Matiere.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  ! Matière non trouvée: {matiere_nom}'))

        # Fonction helper pour créer des exercices
        def create_exercice(topic, question, options, correct_index, difficulte=1, points=10):
            if not topic:
                return None
            exercice, created = Exercice.objects.get_or_create(
                topic=topic,
                question=question,
                defaults={
                    'type_exercice': 'choix_multiple',
                    'options_text': options,
                    'correct_index': correct_index,
                    'difficulte': difficulte,
                    'points_recompense': points,
                    'feedback_success_text': 'Bravo ! Excellente réponse ! ⭐',
                    'feedback_fail_text': 'Pas bon, essaie encore ! Tu peux y arriver !'
                }
            )
            if created:
                self.stdout.write(f'    ✓ Exercice créé: {question[:50]}...')
            return exercice
        
        # --- RÉINTÉGRATION DES EXERCICES CP1/CP2 (Essentiel pour le fonctionnement actuel) ---
        self.stdout.write(self.style.SUCCESS('\nVérification des exercices CP1/CP2...'))

        # CP1
        topic_ecole = Topic.objects.filter(matiere__nom='expression_orale', classe='cp1', titre='Vocabulaire : École et Classe').first()
        create_exercice(topic_ecole, 'Quel objet sert à écrire ?', ['Crayon', 'Chaise', 'Table', 'Fenêtre'], 0, 1)
        create_exercice(topic_ecole, 'Où sommes-nous pour apprendre ?', ['À la maison', 'À l\'école', 'Au marché', 'Au champ'], 1, 1)
        create_exercice(topic_ecole, 'Qui enseigne dans la classe ?', ['L\'élève', 'Le directeur', 'Le maître', 'Le cuisinier'], 2, 2)
        
        topic_corps = Topic.objects.filter(matiere__nom='expression_orale', classe='cp1', titre='Vocabulaire : Corps Humain').first()
        create_exercice(topic_corps, 'Avec quoi vois-tu ?', ['Les oreilles', 'Les yeux', 'Le nez', 'La bouche'], 1, 1)
        create_exercice(topic_corps, 'Combien de doigts as-tu sur une main ?', ['3', '4', '5', '6'], 2, 1)

        topic_nombres = Topic.objects.filter(matiere__nom='mathematiques', classe='cp1', titre='Numération 0-10').first()
        create_exercice(topic_nombres, 'Combien font 2 + 3 ?', ['4', '5', '6', '7'], 1, 1)
        create_exercice(topic_nombres, 'Quel nombre vient après 9 ?', ['8', '9', '10', '11'], 2, 1)
        
        topic_sens = Topic.objects.filter(matiere__nom='sciences', classe='cp1', titre='Les 5 Sens').first()
        create_exercice(topic_sens, 'Avec quel sens goûtes-tu le miel ?', ['La vue', 'L\'ouïe', 'Le goût', 'Le toucher'], 2, 1)
        
        topic_geo = Topic.objects.filter(matiere__nom='mathematiques', classe='cp1', titre='Géométrie : Formes Simples').first()
        create_exercice(topic_geo, 'Quelle forme a 4 côtés égaux ?', ['Cercle', 'Carré', 'Triangle', 'Rectangle'], 1, 1)

        # CP2
        topic_nombres_cp2 = Topic.objects.filter(matiere__nom='mathematiques', classe='cp2', titre='Nombres 0-100').first()
        create_exercice(topic_nombres_cp2, 'Combien font 20 + 30 ?', ['40', '50', '60', '70'], 1, 1)
        create_exercice(topic_nombres_cp2, 'Quel nombre vient après 49 ?', ['48', '49', '50', '51'], 2, 1)
        
        topic_mult = Topic.objects.filter(matiere__nom='mathematiques', classe='cp2', titre='Multiplication : Tables 2,3,4,5').first()
        create_exercice(topic_mult, 'Combien font 2 × 3 ?', ['4', '5', '6', '7'], 2, 1)

        self.stdout.write(self.style.SUCCESS('\n✅ Données complètes chargées avec succès (CP1-CM2) !'))
