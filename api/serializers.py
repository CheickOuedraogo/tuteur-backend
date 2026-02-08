from rest_framework import serializers
from core.models import ProfilEleve, Matiere, Topic, Exercice, Soumission, Progression
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserSignupSerializer(serializers.ModelSerializer):
    classe = serializers.ChoiceField(choices=ProfilEleve.CLASSE_CHOICES)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'classe']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        classe = validated_data.pop('classe')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        ProfilEleve.objects.create(user=user, classe=classe)
        return user


class ProfilEleveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    utilise_ia = serializers.ReadOnlyField()
    
    class Meta:
        model = ProfilEleve
        fields = ['id', 'user', 'classe', 'photo_profil', 'points', 'badges', 'utilise_ia', 'date_creation']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            email = user_data.get('email', user.email)
            
            # Valider l'email unique si changé
            if email != user.email and User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"user": {"email": ["Cet email est déjà utilisé."]}})
            
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = email
            user.save()
            
        return super().update(instance, validated_data)


class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'description', 'image_url', 'audio_intro_url', 'ordre']


class TopicSerializer(serializers.ModelSerializer):
    matiere_nom = serializers.CharField(source='matiere.get_nom_display', read_only=True)
    
    class Meta:
        model = Topic
        fields = ['id', 'matiere', 'matiere_nom', 'classe', 'titre', 'resume', 
                  'image_url', 'audio_url', 'ordre']


class ExerciceSerializer(serializers.ModelSerializer):
    topic_titre = serializers.CharField(source='topic.titre', read_only=True)
    
    class Meta:
        model = Exercice
        fields = ['id', 'topic', 'topic_titre', 'type_exercice', 'question',
                  'question_image_url', 'question_audio_url', 'options_images',
                  'options_text', 'correct_index', 'feedback_success_text',
                  'feedback_success_audio_url', 'feedback_fail_text',
                  'feedback_fail_audio_url', 'difficulte', 'points_recompense',
                  'genere_par_ia']


class SoumissionSerializer(serializers.ModelSerializer):
    exercice_detail = ExerciceSerializer(source='exercice', read_only=True)
    
    class Meta:
        model = Soumission
        fields = ['id', 'eleve', 'exercice', 'exercice_detail', 'reponse_index',
                  'est_correcte', 'score', 'temps_reponse', 'date_soumission']


class ProgressionSerializer(serializers.ModelSerializer):
    topic_detail = TopicSerializer(source='topic', read_only=True)
    taux_reussite = serializers.ReadOnlyField()
    
    class Meta:
        model = Progression
        fields = ['id', 'eleve', 'topic', 'topic_detail', 'score_total',
                  'exercices_reussis', 'exercices_total', 'taux_reussite',
                  'erreurs_consecutives', 'date_derniere_activite']
