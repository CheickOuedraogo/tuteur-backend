"""
Commande de nettoyage : supprime tous les Topics du primaire dont la matière
n'est PAS dans le programme officiel pour cette classe.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Topic
from core.programme_officiel import PROGRAMME_OFFICIEL


class Command(BaseCommand):
    help = 'Supprime les topics hors-programme pour chaque classe'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Afficher les topics à supprimer sans les supprimer',
        )
        parser.add_argument(
            '--classes',
            nargs='+',
            help='Classes à nettoyer (ex: cp1 cp2). Par défaut : toutes.',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        classes_filter = options.get('classes')

        if classes_filter:
            classes = [c.lower() for c in classes_filter]
        else:
            classes = list(PROGRAMME_OFFICIEL.keys())

        total_supprime = 0

        for classe in classes:
            matieres_autorisees = PROGRAMME_OFFICIEL.get(classe, [])
            if not matieres_autorisees:
                self.stdout.write(self.style.WARNING(
                    f"  ⚠ Classe '{classe}' non trouvée dans le programme officiel, ignorée."
                ))
                continue

            # Trouver les topics hors-programme
            topics_hors_programme = Topic.objects.filter(
                classe=classe
            ).exclude(
                matiere__nom__in=matieres_autorisees
            ).select_related('matiere')

            count = topics_hors_programme.count()
            if count == 0:
                self.stdout.write(self.style.SUCCESS(
                    f"  ✓ {classe.upper()} : Aucun topic hors-programme."
                ))
                continue

            self.stdout.write(self.style.WARNING(
                f"  ⚠ {classe.upper()} : {count} topics hors-programme détectés :"
            ))
            for t in topics_hors_programme[:20]:
                self.stdout.write(f"     - [{t.matiere.nom}] {t.titre}")
            if count > 20:
                self.stdout.write(f"     ... et {count - 20} autres")

            if not dry_run:
                with transaction.atomic():
                    deleted, details = topics_hors_programme.delete()
                    total_supprime += deleted
                    self.stdout.write(self.style.SUCCESS(
                        f"     → {deleted} objets supprimés (topics + exercices en cascade)"
                    ))
            else:
                total_supprime += count

        if dry_run:
            self.stdout.write(self.style.NOTICE(
                f"\n🔍 DRY RUN : {total_supprime} topics seraient supprimés. "
                f"Relancez sans --dry-run pour appliquer."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"\n✅ Nettoyage terminé : {total_supprime} objets supprimés."
            ))
