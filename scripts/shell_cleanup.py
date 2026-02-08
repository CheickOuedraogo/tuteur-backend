from core.models import Topic, Matiere

# Définition des matières autorisées par bloc (Inclusion stricte)
PRIMARY_COMMON = ['expression_orale', 'mathematiques', 'sciences', 'ecm', 'langue_nationale', 'anglais', 'eps', 'arts', 'calcul', 'ecriture', 'lecture', 'français', 'francais']
PRIMARY_SUPERIOR = PRIMARY_COMMON + ['histoire', 'geographie', 'tic']

CURRICULUM = {
    'cp1': PRIMARY_COMMON,
    'cp2': PRIMARY_COMMON,
    'ce1': PRIMARY_SUPERIOR,
    'ce2': PRIMARY_SUPERIOR,
    'cm1': PRIMARY_SUPERIOR,
    'cm2': PRIMARY_SUPERIOR,
}

PRIMARY_CLASSES = ['cp1', 'cp2', 'ce1', 'ce2', 'cm1', 'cm2']
topics_to_delete = 0

for topic in Topic.objects.all():
    classe = topic.classe.lower()
    matiere_slug = topic.matiere.nom.lower()
    
    if classe in PRIMARY_CLASSES:
        allowed_matieres = CURRICULUM.get(classe, [])
        # Correction : Correspondance exacte pour éviter que 'sciences_physiques' 
        # ne soit autorisé par 'sciences'
        if matiere_slug not in allowed_matieres:
            print(f"DEL: {topic.titre} ({topic.matiere.nom}) niveau {classe}")
            topic.delete()
            topics_to_delete += 1

    # Matières de lycée/collège (6ème à Terminale)
    if classe not in PRIMARY_CLASSES:
        # Philo à partir de la seconde
        if 'philosophie' in matiere_slug:
            lycee_classes = ['2nde', '1ere_a', '1ere_c', '1ere_d', 't_a', 't_c', 't_d', 'seconde', 'premiere', 'terminale']
            if classe not in lycee_classes:
                print(f"DEL: {topic.titre} ({topic.matiere.nom}) niveau {classe}")
                topic.delete()
                topics_to_delete += 1
                continue

        # Sciences Physiques à partir de la 4ème
        if 'sciences_physiques' in matiere_slug:
            allowed_secondary = ['4eme', '3eme', '2nde', '1ere_a', '1ere_c', '1ere_d', 't_a', 't_c', 't_d', 'seconde', 'premiere', 'terminale']
            if classe not in allowed_secondary:
                print(f"DEL: {topic.titre} ({topic.matiere.nom}) niveau {classe}")
                topic.delete()
                topics_to_delete += 1
                continue

    # Suppression globale de l'arabe (déjà géré mais par sécurité)
    if 'arabe' in matiere_slug:
        print(f"DEL GLO: {topic.titre} ({topic.matiere.nom}) niveau {classe}")
        topic.delete()
        topics_to_delete += 1

print(f"Nettoyage terminé. {topics_to_delete} topics supprimés.")
exit()
