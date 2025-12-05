from django.core.management.base import BaseCommand

from ml_api.models import Dataset 
from ml_core.data_handlers.load_dataset import get_all_dataset_meta
from ml_core.data_handlers.metadata import TaskType


class Command(BaseCommand):
    help = "Synchronize Dataset table with ml_core DatasetMeta definitions."

    def add_arguments(self, parser):
        parser.add_argument(
            "--prune",
            action="store_true",
            help="Delete Dataset rows that do not exist anymore in ml_core.",
        )

    def handle(self, *args, **options):
        prune = options["prune"]

        metas = get_all_dataset_meta()
        seen_codes: set[str] = set()
        created_count = 0
        updated_count = 0

        for meta in metas:
            code = meta.id
            seen_codes.add(code)

            defaults = {
                "name": meta.name,
                "task": meta.task.value,
                "n_samples": meta.n_samples,
                "n_features": meta.n_features,
                "n_classes": meta.n_classes,
                "class_labels": meta.class_labels,
                "feature_names": meta.feature_names,
                "target_name": meta.target_name,
            }

            obj, created = Dataset.objects.update_or_create(
                code=code,
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created dataset {code!r} ({meta.name})")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated dataset {code!r} ({meta.name})")
                )

        deleted_count = 0
        if prune:
            qs_to_delete = Dataset.objects.exclude(code__in=seen_codes)
            deleted_count = qs_to_delete.count()
            if deleted_count:
                qs_to_delete.delete()
                self.stdout.write(
                    self.style.ERROR(
                        f"Pruned {deleted_count} datasets not present in ml_core."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync finished. Created: {created_count}, updated: {updated_count}, "
                f"pruned: {deleted_count}."
            )
        )
