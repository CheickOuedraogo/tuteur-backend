from django.contrib import admin
from .models import ProfilEleve, Matiere, Topic, Exercice, Soumission, Progression


@admin.register(ProfilEleve)
class ProfilEleveAdmin(admin.ModelAdmin):
    list_display = ['user', 'classe', 'points', 'badges', 'date_creation']
    list_filter = ['classe', 'date_creation']
    search_fields = ['user__username', 'user__email']


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre', 'image_url']
    ordering = ['ordre']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['titre', 'matiere', 'classe', 'ordre']
    list_filter = ['matiere', 'classe']
    ordering = ['matiere', 'classe', 'ordre']


@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display = ['question', 'topic', 'type_exercice', 'difficulte', 'genere_par_ia']
    list_filter = ['topic__matiere', 'topic__classe', 'type_exercice', 'genere_par_ia']
    search_fields = ['question', 'topic__titre']


@admin.register(Soumission)
class SoumissionAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'exercice', 'est_correcte', 'score', 'date_soumission']
    list_filter = ['est_correcte', 'date_soumission']
    search_fields = ['eleve__user__username']


@admin.register(Progression)
class ProgressionAdmin(admin.ModelAdmin):
    list_display = ['eleve', 'topic', 'taux_reussite', 'exercices_reussis', 'exercices_total']
    list_filter = ['topic__matiere', 'topic__classe']
    search_fields = ['eleve__user__username']
