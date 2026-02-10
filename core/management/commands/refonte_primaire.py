import random
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Matiere, Topic, Exercice
from core.programme_officiel import PROGRAMME_OFFICIEL_PRIMAIRE

class Command(BaseCommand):
    help = 'Refonte STRÍCTE du programme primaire (CP1-CM2) avec AEC et sans EPS'

    def handle(self, *args, **kwargs):
        self.stdout.write("Démarrage de la refonte STRÍCTE du programme primaire...")
        
        # Définition du programme COMPLET (Strictement basé sur la liste utilisateur)
        PROGRAMME = {
            'cp1': {
                'lecture': [
                    ("Reconnaissance des voyelles (a, e, i, o, u)", "Les voyelles sont les sons qui font chanter les mots."),
                    ("Apprentissage des consonnes simples", "Les consonnes s'unissent aux voyelles."),
                    ("Formation de syllabes", "Une consonne + une voyelle = une syllabe."),
                    ("Lecture de mots simples", "Exemple : papa, maman, pipe."),
                    ("Déchiffrage de phrases courtes", "Exemple : Toto va à l'école.")
                ],
                'ecriture': [
                    ("Tenue correcte du crayon", "Bien tenir son crayon avec 3 doigts."),
                    ("Traçage des voyelles", "Tracer proprement les voyelles."),
                    ("Écriture des consonnes", "Écrire les consonnes usuelles."),
                    ("Formation de syllabes et mots", "Attacher les lettres pour former des mots."),
                    ("Copie de mots du tableau", "Recopier sans fautes.")
                ],
                'exercices_sensoriels': [
                    ("Distinction des couleurs", "Reconnaître les couleurs de base."),
                    ("Distinction des formes", "Rond, carré, triangle."),
                    ("Disposition dans l'espace", "Devant, derrière, dessus, dessous."),
                    ("Reconnaissance de tailles", "Grand, petit, moyen."),
                    ("Organisation spatiale", "Gauche et droite.")
                ],
                'expression_orale': [
                    ("Formules de politesse", "Bonjour, merci, au revoir."),
                    ("Présentation personnelle", "Nom, âge, famille."),
                    ("Vocabulaire de l'école", "Classe, tableau, craie."),
                    ("Parties du corps humain", "La tête, les membres, le tronc."),
                    ("Objets de la maison", "Nommer les objets usuels.")
                ],
                'arithmetique': [
                    ("Nombres de 0 à 20", "Compter et reconnaître les chiffres."),
                    ("Comptage d'objets", "Dénombrer une collection."),
                    ("Comparaison de quantités", "Plus, moins, autant."),
                    ("Additions simples", "Calculer de petites sommes."),
                    ("Tracés de lignes", "Lignes droites et courbes.")
                ],
                'exercices_observation': [
                    ("Le monde vivant", "Introduction aux plantes et animaux."),
                    ("Le corps humain", "Observation simple.")
                ],
                'aec': [
                    ("Dessin libre", "S'exprimer par le dessin."),
                    ("Chants patriotiques", "Apprendre l'Hymne National."),
                    ("Musique et rythmes", "Taper dans les mains, suivre un rythme."),
                    ("Arts plastiques", "Modelage et collage simple."),
                    ("Travaux manuels", "Pliage et découpage.")
                ]
            },
            'cp2': {
                'lecture': [
                    ("Sons composés (ou, on, an...)", "Lire des sons complexes."),
                    ("Articulations difficiles", "S'entraîner sur les sons ch, ph, gn."),
                    ("Lecture de phrases", "Fluidifier la lecture."),
                    ("Compréhension simple", "Raconter ce qu'on a lu."),
                    ("Lecture expressive", "Mettre le ton.")
                ],
                'ecriture': [
                    ("Écriture cursive", "Fluidité du geste."),
                    ("Copie de textes", "Recopier sans erreurs."),
                    ("Dictée de mots", "Écrire sous la dictée."),
                    ("Orthographe visuelle", "Retenir les mots courants."),
                    ("Production de phrases", "Écrire une petite phrase.")
                ],
                'expression_orale': [
                    ("Description d'images", "S'exprimer sur un visuel."),
                    ("Récitation", "Apprendre des poèmes du Burkina."),
                    ("Vocabulaire thématique", "La famille et les aliments."),
                    ("Narration", "Raconter un événement."),
                    ("Répondre au maître", "Dialoguer en classe.")
                ],
                'arithmetique': [
                    ("Nombres de 0 à 100", "Maîtriser les dizaines."),
                    ("Addition et soustraction posées", "Colonnes et calculs."),
                    ("Tables d'addition", "Apprendre par cœur."),
                    ("Problèmes simples", "Réflexion mathématique."),
                    ("Doubles et moitiés", "Calcul mental rapide.")
                ],
                'exercices_observation': [
                    ("Les cinq sens", "Vue, ouïe, odorat, goût, toucher."),
                    ("Hygiène corporelle", "Se laver, brosser les dents."),
                    ("Animaux domestiques/sauvages", "Connaître notre faune."),
                    ("Les plantes utiles", "Agriculture et nutrition."),
                    ("Saisons et météo", "Le climat au Burkina.")
                ],
                'aec': [
                    ("Dessin technique", "Reproduire des formes."),
                    ("Chants burkinabè", "Répertoire culturel."),
                    ("Instruments traditionnels", "Introduction à la musique locale."),
                    ("Arts plastiques", "Peinture et collage."),
                    ("Travaux manuels", "Initiation au tressage/pliage.")
                ]
            },
            'ce1': {
                'lecture': [
                    ("Lecture courante", "Lire sans hésiter."),
                    ("Compréhension récit", "Analyser une histoire."),
                    ("Action et personnages", "Comprendre l'intrigue."),
                    ("Lecture haute voix", "Partager sa lecture."),
                    ("Textes documentaires", "Informations réelles.")
                ],
                'ecriture': [
                    ("Écriture soignée", "Beauté de la lettre."),
                    ("Copie rapide", "Efficacité du geste.")
                ],
                'grammaire': [
                    ("La phrase", "Sujet + Verbe."),
                    ("Le nom", "Propre et commun."),
                    ("Le déterminant", "Articles définis/indéfinis."),
                    ("L'adjectif", "Qualifier le nom."),
                    ("Le verbe", "Identifier l'action.")
                ],
                'conjugaison': [
                    ("Présent (1er groupe)", "Actions actuelles."),
                    ("Futur simple", "Actions futures."),
                    ("Passé composé", "Actions passées."),
                    ("Être et Avoir", "Conjuguer les auxiliaires."),
                    ("Identifier le temps", "Passé, présent, futur.")
                ],
                'orthographe': [
                    ("Mots usuels", "Vocabulaire courant."),
                    ("Masculin/Féminin", "Le genre."),
                    ("Singulier/Pluriel", "Le nombre."),
                    ("Homophones (a/à)", "Confusion courante."),
                    ("Ponctuation", "Points et virgules.")
                ],
                'vocabulaire': [
                    ("Famille de mots", "Mots dérivés."),
                    ("Synonymes", "Mots proches."),
                    ("Contraires", "Mots opposés."),
                    ("Ordre alphabétique", "Ranger dans le dico."),
                    ("Sens du mot", "Contexte de la phrase.")
                ],
                'expression_orale': [
                    ("Dialogues", "Échanger en classe."),
                    ("Explication", "Clarifier un propos.")
                ],
                'arithmetique': [
                    ("Jusqu'à 1000", "Unités, dizaines, centaines."),
                    ("Retenues", "Add/Sub avec retenues."),
                    ("Multiplication", "Addition répétée."),
                    ("Tables 2 à 5", "Connaissance rapide."),
                    ("Problèmes simples", "Une étape de calcul.")
                ],
                'geometrie': [
                    ("Droites", "Utilisation de la règle."),
                    ("Formes planes", "Carré, triangle, cercle."),
                    ("Figures usuelles", "Propriétés simples.")
                ],
                'systeme_metrique': [
                    ("Mètre", "Mesurer des longueurs."),
                    ("Kilogramme", "Mesurer des masses."),
                    ("Litre", "Mesurer des volumes."),
                    ("Heure", "Introduction à la pendule.")
                ],
                'exercices_observation': [
                    ("Nutrition", "Équilibre alimentaire."),
                    ("Dents", "Structure et soin."),
                    ("Respiration", "L'air et les poumons."),
                    ("Vivant/Non-vivant", "Distinguer la vie."),
                    ("Usage de l'eau", "L'eau dans la vie.")
                ],
                'geographie': [
                    ("L'école", "Espace scolaire."),
                    ("Quartier/Village", "Vie locale."),
                    ("Points cardinaux", "S'orienter."),
                    ("Plan classe", "Représentation simple."),
                    ("Burkina Faso", "Frontières et carte.")
                ],
                'histoire': [
                    ("Le temps qui passe", "Hier, aujourd'hui."),
                    ("Anciens du village", "Transmission orale.")
                ],
                'ecm': [
                    ("Respect", "Politesse sociale."),
                    ("Règles d'école", "Vivre ensemble."),
                    ("Famille", "Respect des aînés."),
                    ("Droits enfant", "Protection."),
                    ("Le drapeau", "Signification des couleurs.")
                ],
                'aec': [
                    ("Dessin", "Ombres et lumières."),
                    ("Hymne National", "Le Ditanyè."),
                    ("Arts plastiques", "Décoration."),
                    ("Chant traditionnel", "Culture locale.")
                ]
            },
            'ce2': {
                'lecture': [
                    ("Textes narratifs", "Récits structurés."),
                    ("Analyse texte", "Compréhension fine."),
                    ("Thème principal", "Sujet central."),
                    ("Vocabulaire riche", "Nouveaux termes."),
                    ("Lecture expressive", "Nuances de voix.")
                ],
                'grammaire': [
                    ("Groupe sujet/verbal", "Structure complexe."),
                    ("COD", "Complément direct."),
                    ("Adverbes", "Manière, temps."),
                    ("Types de phrases", "Interrogation, exclamation."),
                    ("Négation", "Ne... pas.")
                ],
                'conjugaison': [
                    ("Imparfait", "Temps du passé."),
                    ("Futur/Présent", "Consolidation."),
                    ("Passé composé", "Verbes fréquents."),
                    ("2ème groupe", "Verbes en -ir."),
                    ("Impératif", "Ordre et conseil.")
                ],
                'orthographe': [
                    ("Sujet-Verbe", "Règles d'accord."),
                    ("Groupe Nominal", "Accords pluriels."),
                    ("Homophones (son/sont)", "Savoir distinguer."),
                    ("Mots invariables", "Apprendre par cœur."),
                    ("Lettres muettes", "Fin de mots.")
                ],
                'vocabulaire': [
                    ("Affixes", "Préfixes et suffixes."),
                    ("Propre/Figuré", "Deux sens."),
                    ("Expressions", "Langue imagée."),
                    ("Champs lexicaux", "Globalité du sens."),
                    ("Dictionnaire", "Vitesse de recherche.")
                ],
                'expression_orale': [
                    ("Exposé", "Parler seul devant les autres."),
                    ("Débat", "Donner son avis.")
                ],
                'expression_ecrite': [
                    ("Phrases complexes", "Emploi des conjonctions."),
                    ("Descriptions", "Portrait et lieux."),
                    ("Chronologie", "Ordre des actions."),
                    ("Petits récits", "Écriture créative."),
                    ("Lettre", "Format courrier.")
                ],
                'arithmetique': [
                    ("Jusqu'à 10 000", "Les grands nombres."),
                    ("Quatre opérations", "Pratique intensive."),
                    ("Tables totales", "Zéro hésitation."),
                    ("Division simple", "Partage égal."),
                    ("Problèmes à 2 étapes", "Chaîner le raisonnement.")
                ],
                'geometrie': [
                    ("Angles droits", "Usage de l'équerre."),
                    ("Polygones", "Propriétés avancées."),
                    ("Périmètre", "Calcul du tour."),
                    ("Symétrie", "Axes et figures."),
                    ("Compas", "Cercles et arcs.")
                ],
                'systeme_metrique': [
                    ("Conversions", "M à Cm."),
                    ("Masses", "Kg et G."),
                    ("Capacités", "L et Cl."),
                    ("Calendrier", "Le temps long."),
                    ("Franc CFA", "Calcul financier.")
                ],
                'sciences': [
                    ("Digestion", "Trajet digestif."),
                    ("Circulation", "Cœur et sang."),
                    ("Squelette", "Os et muscles."),
                    ("Végétaux", "Croissance plante."),
                    ("Pollution", "Dangers pour la nature.")
                ],
                'geographie': [
                    ("Régions du Burkina", "Les 13 régions."),
                    ("Relief/Eau", "Fleuves et monts."),
                    ("Climat", "Harmattan et mousson."),
                    ("Villes", "Villes principales."),
                    ("Économie", "Agriculture/Élevage.")
                ],
                'histoire': [
                    ("Pre-colonisation", "Royaumes anciens."),
                    ("Cultures locales", "Tradition et modernité.")
                ],
                'ecm': [
                    ("Institutions", "L'État burkinabè."),
                    ("Solidarité", "Aide mutuelle."),
                    ("Éco-gestes", "Respect nature."),
                    ("Sécurité routière", "Piétons."),
                    ("Santé", "Lutte contre maladies.")
                ],
                'aec': [
                    ("Photographie simple", "Cadrer une vue."),
                    ("Théâtre/Mime", "Expression corporelle."),
                    ("Chant chorale", "Collectif."),
                    ("Artisanat", "Découverte des métiers.")
                ]
            },
            'cm1': {
                'lecture': [
                    ("Littérature", "Extraits de romans."),
                    ("Analyse", "Critique littéraire."),
                    ("Idée principale", "Synthèse."),
                    ("Vocabulaire", "Mots soutenus."),
                    ("Argumentation", "Lecture active.")
                ],
                'grammaire': [
                    ("Subordonnées", "Phrases liées."),
                    ("Compléments", "Lieu, Temps, Manière."),
                    ("Pronoms", "Usage complexe."),
                    ("Voix active/passive", "Transformer la phrase."),
                    ("Expansion du nom", "Relative et complément nom.")
                ],
                'conjugaison': [
                    ("Passé simple", "Récit historique."),
                    ("Plus-que-parfait", "Passé lointain."),
                    ("Conditionnel", "Souhait et condition."),
                    ("3ème groupe", "Verbes complexes."),
                    ("Participes", "Formes verbales.")
                ],
                'orthographe': [
                    ("Mots complexes", "Orthographe lexicale."),
                    ("Accords Participes", "Règles précises."),
                    ("Homophones", "S'en, sans, etc."),
                    ("Pluriel Composés", "Des porte-plumes."),
                    ("Radicaux", "Racines des mots.")
                ],
                'vocabulaire': [
                    ("Registres", "Familier à soutenu."),
                    ("Métaphores", "Figures de style."),
                    ("Terminologie", "Mots techniques."),
                    ("Étymologie", "Origine grecque/latine."),
                    ("Documentation", "Encyclopédie et web.")
                ],
                'expression_orale': [
                    ("Exposé structuré", "Présenter un sujet."),
                    ("Débat d'idées", "Échanger avec respect."),
                    ("Compte-rendu", "Rapport d'activité."),
                    ("Stratégie orale", "Convaincre."),
                    ("Élocution", "Clarté du débit.")
                ],
                'expression_ecrite': [
                    ("Schéma narratif", "Début, milieu, fin."),
                    ("Portrait moral", "Psychologie personnage."),
                    ("Dialogues riches", "Dramaturgie."),
                    ("Lettre officielle", "Demande administrative."),
                    ("Résumé long", "Dégager l'essentiel.")
                ],
                'arithmetique': [
                    ("Millions", "Les très grands nombres."),
                    ("Décimaux", "Opérer avec la virgule."),
                    ("Fractions", "Base et calculs."),
                    ("Proportionnalité", "Échanges et vitesses."),
                    ("Problèmes complexes", "Savoir analyser.")
                ],
                'geometrie': [
                    ("Cercle", "Termes techniques."),
                    ("Aires", "Rectangle et carré."),
                    ("Volumes", "Capacité spatiale."),
                    ("Constructions", "Géométrie exacte."),
                    ("Échelles", "Plans et cartes.")
                ],
                'systeme_metrique': [
                    ("Tableaux", "Conversions expertes."),
                    ("M², Cm²", "Surfaces."),
                    ("M³, L", "Volumes réels."),
                    ("Km/h", "Calcul de vitesse."),
                    ("Applications", "Cas réels.")
                ],
                'sciences': [
                    ("Reproduction", "Base du vivant."),
                    ("Électricité", "Circuits et dangers."),
                    ("Aimants", "Forces invisibles."),
                    ("États Matière", "Solide/Liquide/Gaz."),
                    ("Biodiversité", "Chaînes de vie.")
                ],
                'geographie': [
                    ("CEDEAO", "Intégration régionale."),
                    ("Physique Burkina", "Relief et fleuves."),
                    ("Ressources", "Or et coton."),
                    ("Population", "Démographie."),
                    ("Modernité", "Infrastructures.")
                ],
                'histoire': [
                    ("Mogho Naba", "Histoire des Mossi."),
                    ("Colonisation", "Changements politiques."),
                    ("Indépendance", "La République."),
                    ("Héros nationaux", "Ouezzin, Yaméogo."),
                    ("Politique actuelle", "Le présent.")
                ],
                'ecm': [
                    ("Administration", "Provinces/Communes."),
                    ("Citoyenneté", "Voter."),
                    ("Justice", "Tribunaux."),
                    ("Prévention", "Maladies contagieuses."),
                    ("Durable", "Solaire et arbres.")
                ],
                'aec': [
                    ("Peinture", "Mélange des couleurs."),
                    ("Musique", "Solfège de base."),
                    ("Patrimoine", "Masques et danses."),
                    ("Expression corporelle", "Danse et mime.")
                ],
                'tic': [
                    ("Matériel", "Clavier, souris, écran."),
                    ("Bureautique", "Ouvrir un logiciel.")
                ]
            },
            'cm2': {
                'lecture': [
                    ("Critique", "Juger un texte."),
                    ("Synthèse", "Regrouper les infos."),
                    ("Autonomie", "Lire beaucoup."),
                    ("Examen CEP", "Annales lecture."),
                    ("Littérature Faso", "Auteurs nationaux.")
                ],
                'grammaire': [
                    ("Analyse complète", "Syntaxe totale."),
                    ("Relatives", "Propositions complexes."),
                    ("Passive", "Maîtrise complète."),
                    ("Discours", "Direct et indirect."),
                    ("Fonctions", "Attributs du sujet.")
                ],
                'conjugaison': [
                    ("Indicatif total", "Huit temps."),
                    ("Subjonctif", "Le mode de l'incertain."),
                    ("Conditionnel passé", "Regret."),
                    ("Concordance", "Temps du récit."),
                    ("Passé simple", "Verbes du 3eme groupe.")
                ],
                'orthographe': [
                    ("Vocabulaire CEP", "Mots difficiles."),
                    ("Tous Accords", "Zéro faute."),
                    ("Homophones", "Cas particuliers."),
                    ("Règles orthographe", "Exceptions."),
                    ("Dictées CEP", "Vitesse et soin.")
                ],
                'vocabulaire': [
                    ("Abstrait", "Mots complexes."),
                    ("Néologismes", "Evolution langue."),
                    ("Formation", "Composition mots."),
                    ("Précision", "Termes exacts."),
                    ("Lexique CEP", "Préparation.")
                ],
                'expression_orale': [
                    ("Projet personnel", "Présentation."),
                    ("Arguments", "Logique orale."),
                    ("Synthèse", "Clarté du message."),
                    ("Formel", "S'adresser au jury."),
                    ("Oral CEP", "Épreuve finale.")
                ],
                'expression_ecrite': [
                    ("Rédaction longue", "Développement."),
                    ("Complexité", "Style et syntaxe."),
                    ("Persuasion", "Convaincre."),
                    ("Comptes rendus", "Évènements."),
                    ("Styles variés", "Journalisme, administratif.")
                ],
                'arithmetique': [
                    ("Décimaux avancés", "Opérations expertes."),
                    ("Calcul fractions", "Multiplication/Division."),
                    ("Pourcentages", "Intérêts et baisses."),
                    ("Budget", "Gestion quotidienne."),
                    ("Épreuves CEP", "Sujets type.")
                ],
                'geometrie': [
                    ("Constructions", "Figures complexes."),
                    ("Aires/Périmètres", "Problème mélange."),
                    ("Solides", "Patrons et volumes."),
                    ("Translation", "Glissement figure."),
                    ("Réflexion", "Application pratique.")
                ],
                'systeme_metrique': [
                    ("Maîtrise totale", "Vitesse conversion."),
                    ("Composées", "Unités mixtes."),
                    ("Terrain", "Arpentage."),
                    ("Problèmes", "Logique de mesure."),
                    ("Préparation CEP", "Révision finale.")
                ],
                'sciences': [
                    ("Systèmes humains", "Circulation, nerveux."),
                    ("Énergies au Faso", "Solaire et eau."),
                    ("Écologie", "Le Sahel."),
                    ("Technologie", "Machines simples."),
                    ("Méthode", "Démarche expérimentale.")
                ],
                'geographie': [
                    ("Afrique", "Pays et capitales."),
                    ("Le Monde", "Cinq continents."),
                    ("Commerce", "Échanges mondiaux."),
                    ("Climat mondial", "Réchauffement."),
                    ("Défis", "Eau et faim.")
                ],
                'histoire': [
                    ("Synthèse Burkina", "Grands évènements."),
                    ("Afrique coloniale", "Résistance."),
                    ("Histoire Mondiale", "Grandes étapes."),
                    ("Mandela / Sankara", "Grands hommes."),
                    ("Tradition", "Patrimoine mondial UNESCO.")
                ],
                'ecm': [
                    ("Constitution", "La Loi Mère."),
                    ("Internationale", "ONU, UA, CEDEAO."),
                    ("Droits Humains", "Égalité."),
                    ("Responsabilité", "Sens civique."),
                    ("Vers le Collège", "Autonomie.")
                ],
                'aec': [
                    ("Muséographie", "Visite virtuelle."),
                    ("Art contemporain", "Sculpture."),
                    ("Cuisine", "Nutrition et tradition."),
                    ("Projet AEC", "Création finale.")
                ],
                'tic': [
                    ("Traitement texte", "Rédiger une page."),
                    ("Internet", "Navigation sécurisée."),
                    ("Email", "Envoyer un message."),
                    ("Éthique", "Comportement web."),
                    ("Savoir-faire", "Outils numériques.")
                ]
            }
        }

        # CLASSES PRIMAIRES
        CLASSES_PRIMAIRES = ['cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2']

        with transaction.atomic():
            self.stdout.write("Nettoyage RADICAL des anciens contenus du primaire...")
            Topic.objects.filter(classe__in=CLASSES_PRIMAIRES).delete()

            for classe, matieres_dict in PROGRAMME.items():
                self.stdout.write(f"Création de la classe {classe}...")
                
                for matiere_nom, topics_list in matieres_dict.items():
                    matiere_obj, _ = Matiere.objects.get_or_create(
                        nom=matiere_nom,
                        defaults={'description': f'Matière {matiere_nom}'}
                    )
                    
                    ordre_topic = 1
                    for titre, resume in topics_list:
                        topic = Topic.objects.create(
                            matiere=matiere_obj,
                            classe=classe,
                            titre=titre,
                            resume=resume,
                            contenu_cours=resume,
                            ordre=ordre_topic
                        )
                        ordre_topic += 1
                        self.generer_qcm(topic)

            # Nettoyage post-création : supprimer les topics hors-programme
            self.stdout.write("Nettoyage des topics hors-programme officiel...")
            for classe_code in CLASSES_PRIMAIRES:
                matieres_ok = PROGRAMME_OFFICIEL_PRIMAIRE.get(classe_code, [])
                if matieres_ok:
                    orphelins = Topic.objects.filter(classe=classe_code).exclude(matiere__nom__in=matieres_ok)
                    count = orphelins.count()
                    if count > 0:
                        orphelins.delete()
                        self.stdout.write(f"  → {classe_code.upper()}: {count} topics hors-programme supprimés")

        self.stdout.write(self.style.SUCCESS(f'Refonte terminée ! {Topic.objects.filter(classe__in=CLASSES_PRIMAIRES).count()} topics primaires créés.'))

    def generer_qcm(self, topic):
        """Génère 3 questions simples basées sur le sujet"""
        
        questions = [
            {
                'question': f"La leçon d'aujourd'hui s'appelle '{topic.titre}'. De quoi parle-t-elle ?",
                'options': [f"{topic.resume[:50]}...", "De rien", "D'un autre sujet"],
                'correct': 0,
                'feedback': f"C'est ça ! {topic.resume}"
            },
            {
                'question': f"Est-ce que '{topic.titre}' est important pour ton avenir ?",
                'options': ["Oui, beaucoup !", "Non", "Je ne sais pas"],
                'correct': 0,
                'feedback': "Exactement, chaque leçon compte pour devenir plus fort !"
            },
             {
                'question': "Quelle est la meilleure chose à faire en classe ?",
                'options': ["Écouter le maître", "Jouer au ballon", "Dormir"],
                'correct': 0,
                'feedback': "Bravo ! L'écoute est la clé de la réussite."
            }
        ]

        for q in questions:
            Exercice.objects.create(
                topic=topic,
                type_exercice='choix_multiple',
                question=q['question'],
                options_text=q['options'],
                correct_index=q['correct'],
                points_recompense=10,
                feedback_success_text=q['feedback']
            )
