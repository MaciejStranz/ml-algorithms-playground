from django.core.management.base import BaseCommand

from ml_api.models import Algorithm  # adjust import if your app name is different
from ml_core.algorithms.registry import get_all_algorithms_meta


class Command(BaseCommand):
    help = "Synchronize Algorithm table with ml_core algorithm registry."

    def add_arguments(self, parser):
        parser.add_argument(
            "--prune",
            action="store_true",
            help="Delete Algorithm rows that are no longer present in ml_core.",
        )

    def handle(self, *args, **options):
        prune = options["prune"]

        meta_list = get_all_algorithms_meta()
        seen_codes: set[str] = set()
        created_count = 0
        updated_count = 0

        for meta in meta_list:
            code = meta["code"]
            seen_codes.add(code)

            defaults = {
                "name": meta["name"],
                "kind": meta["kind"],
                "description": meta.get("description", ""),
                "hyperparameter_specs": meta["hyperparameter_specs"],
            }

            obj, created = Algorithm.objects.update_or_create(
                code=code,
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created algorithm {code!r} ({obj.name})")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated algorithm {code!r} ({obj.name})")
                )

        deleted_count = 0
        if prune:
            qs_to_delete = Algorithm.objects.exclude(code__in=seen_codes)
            deleted_count = qs_to_delete.count()
            if deleted_count:
                qs_to_delete.delete()
                self.stdout.write(
                    self.style.ERROR(
                        f"Pruned {deleted_count} algorithms not present in ml_core."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Algorithm sync finished. Created: {created_count}, "
                f"updated: {updated_count}, pruned: {deleted_count}."
            )
        )
