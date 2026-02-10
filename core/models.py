from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class ProfilEleve(models.Model):
    """Profil d'un élève avec sa classe et progression"""
    CLASSE_CHOICES = [
        ('cp1', 'CP1'),
        ('cp2', 'CP2'),
        ('ce1', 'CE1'),
        ('ce2', 'CE2'),
        ('cm1', 'CM1'),
        ('cm2', 'CM2'),
        ('6eme', '6ème'),
        ('5eme', '5ème'),
        ('4eme', '4ème'),
        ('3eme', '3ème'),
        ('2nde', '2nde'),
        ('1ere_a', '1ère A'),
        ('1ere_c', '1ère C'),
        ('1ere_d', '1ère D'),
        ('t_a', 'Terminale A'),
        ('t_c', 'Terminale C'),
        ('t_d', 'Terminale D'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_eleve')
    classe = models.CharField(max_length=10, choices=CLASSE_CHOICES)
    photo_profil = models.ImageField(upload_to='avatars/', null=True, blank=True)
    points = models.IntegerField(default=0)
    badges = models.JSONField(default=list, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    @property
    def utilise_ia(self):
        """Détermine si cette classe utilise l'IA textuelle (Sandy Chat).
        CP1 et CP2 utilisent Sandy en mode vocal uniquement.
        """
        return self.classe not in ['cp1', 'cp2']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_classe_display()}"


class Matiere(models.Model):
    """Matière scolaire (Expression Orale, Mathématiques, etc.)"""
    NOM_MATIERES = [
        ('francais', 'Français'),
        ('lecture', 'Lecture'),
        ('litterature', 'Littérature'),
        ('ecriture', 'Écriture'),
        ('grammaire', 'Grammaire'),
        ('conjugaison', 'Conjugaison'),
        ('orthographe', 'Orthographe'),
        ('vocabulaire', 'Vocabulaire'),
        ('expression_orale', 'Expression Orale'),
        ('expression_ecrite', 'Expression Écrite'),
        ('mathematiques', 'Mathématiques'),
        ('arithmetique', 'Arithmétique'),
        ('geometrie', 'Géométrie'),
        ('systeme_metrique', 'Système Métrique'),
        ('sciences', 'Sciences'),
        ('exercices_sensoriels', 'Exercices Sensoriels'),
        ('exercices_observation', 'Exercices d\'Observation'),
        ('histoire', 'Histoire'),
        ('geographie', 'Géographie'),
        ('ecm', 'Éducation Civique et Morale'),
        ('aec', 'Activités d\'Expression et de Création (AEC)'),
        ('arts', 'Arts et Culture'),
        ('anglais', 'Anglais'),
        ('svt', 'SVT'),
        ('physique_chimie', 'Physique-Chimie'),
        ('philosophie', 'Philosophie'),
        ('tic', 'Informatique (TIC)'),
    ]
    
    nom = models.CharField(max_length=50, choices=NOM_MATIERES, unique=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True, help_text="URL de l'image pour l'accueil")
    audio_intro_url = models.URLField(blank=True, null=True, help_text="URL audio d'introduction")
    ordre = models.IntegerField(default=0, help_text="Ordre d'affichage")
    
    def __str__(self):
        return self.get_nom_display()


class Topic(models.Model):
    """Thème/Sujet dans une matière (ex: Nombres 0-20 pour Math CP1)"""
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='topics')
    classe = models.CharField(max_length=10, choices=ProfilEleve.CLASSE_CHOICES)
    titre = models.CharField(max_length=200)
    resume = models.TextField(help_text="Résumé du contenu du thème")
    contenu_cours = models.TextField(blank=True, null=True, help_text="Contenu détaillé du cours (généré par IA)")
    image_url = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True, help_text="URL audio d'explication")
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['matiere', 'classe', 'ordre']
        unique_together = [['matiere', 'classe', 'titre']]
    
    def __str__(self):
        return f"{self.matiere.get_nom_display()} - {self.classe.upper()} - {self.titre}"


class Exercice(models.Model):
    """Exercice interactif (pré-généré pour CP1/CP2, ou généré par IA pour >CP2)"""
    TYPE_EXERCICE = [
        ('choix_multiple', 'Choix Multiple (Images)'),
        ('drag_drop', 'Drag & Drop'),
        ('calcul', 'Calcul'),
        ('observation', 'Observation'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='exercices')
    type_exercice = models.CharField(max_length=20, choices=TYPE_EXERCICE)
    question = models.TextField(help_text="Question textuelle")
    question_image_url = models.URLField(blank=True, null=True, help_text="Image de la question")
    question_audio_url = models.URLField(blank=True, null=True, help_text="Audio de la question")
    
    # Pour CP1/CP2: options pré-générées
    options_images = models.JSONField(
        default=list, 
        blank=True,
        help_text="Liste d'URLs d'images pour les options (CP1/CP2)"
    )
    options_text = models.JSONField(
        default=list,
        blank=True,
        help_text="Liste de textes pour les options"
    )
    correct_index = models.IntegerField(help_text="Index de la réponse correcte (0-based)")
    
    # Feedback
    feedback_success_text = models.TextField(default="Bravo ! Excellente réponse !")
    feedback_success_audio_url = models.URLField(blank=True, null=True)
    feedback_fail_text = models.TextField(default="Pas bon, essaie encore !")
    feedback_fail_audio_url = models.URLField(blank=True, null=True)
    
    # Adaptation
    difficulte = models.IntegerField(default=1, help_text="1=Facile, 2=Moyen, 3=Difficile")
    points_recompense = models.IntegerField(default=10)
    
    # Pour IA (>CP2)
    genere_par_ia = models.BooleanField(default=False)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['topic', 'difficulte', 'date_creation']
    
    def __str__(self):
        return f"{self.topic} - {self.question[:50]}..."


class Soumission(models.Model):
    """Soumission d'un exercice par un élève"""
    eleve = models.ForeignKey(ProfilEleve, on_delete=models.CASCADE, related_name='soumissions')
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, related_name='soumissions')
    reponse_index = models.IntegerField(help_text="Index de la réponse choisie")
    est_correcte = models.BooleanField()
    score = models.IntegerField(default=0, help_text="Points obtenus")
    temps_reponse = models.IntegerField(blank=True, null=True, help_text="Temps en secondes")
    date_soumission = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_soumission']
        indexes = [
            models.Index(fields=['eleve', 'date_soumission']),
            models.Index(fields=['exercice', 'est_correcte']),
        ]
    
    def __str__(self):
        status = "✓" if self.est_correcte else "✗"
        return f"{self.eleve.user.username} - {status} - {self.exercice}"


class Progression(models.Model):
    """Suivi de progression par matière/topic pour un élève"""
    eleve = models.ForeignKey(ProfilEleve, on_delete=models.CASCADE, related_name='progressions')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='progressions')
    score_total = models.IntegerField(default=0)
    exercices_reussis = models.IntegerField(default=0)
    exercices_total = models.IntegerField(default=0)
    erreurs_consecutives = models.IntegerField(default=0, help_text="Pour adaptation CP1/CP2")
    date_derniere_activite = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['eleve', 'topic']]
        ordering = ['-date_derniere_activite']
    
    @property
    def taux_reussite(self):
        if self.exercices_total == 0:
            return 0.0
        return (self.exercices_reussis / self.exercices_total) * 100
    
    def __str__(self):
        return f"{self.eleve.user.username} - {self.topic} - {self.taux_reussite:.1f}%"
