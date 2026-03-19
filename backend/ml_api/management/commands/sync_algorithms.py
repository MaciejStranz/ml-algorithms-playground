from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from ml_api.models import Algorithm, AlgorithmVariant


class Command(BaseCommand):
    help = "Sync algorithms + variants metadata from ml_core into Django DB."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-clean",
            action="store_true",
            help="Do not delete DB variants missing in ml_core export.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        from ml_core.algorithms.catalog import export_algorithms_for_backend

        payload = export_algorithms_for_backend()
        if not isinstance(payload, list):
            raise RuntimeError("ml_core export must return a list of algorithms.")

        no_clean = bool(options.get("no_clean"))

        seen_algo_codes: set[str] = set()
        seen_variant_codes: set[str] = set()

        created_algos = updated_algos = 0
        created_vars = updated_vars = 0

        for algo in payload:
            code = algo["code"]
            defaults = {
                "name": algo.get("name", code),
                "kind": algo.get("kind", "classical"),
                "description": algo.get("description", ""),
            }

            algo_obj, created = Algorithm.objects.update_or_create(code=code, defaults=defaults)
            seen_algo_codes.add(code)
            created_algos += int(created)
            updated_algos += int(not created)

            for v in algo.get("variants", []):
                v_code = v["code"]
                v_defaults = {
                    "algorithm": algo_obj,
                    "supported_tasks": v.get("supported_tasks", []),
                    "hyperparameter_specs": v.get("hyperparameter_specs", []),
                }

                v_obj, v_created = AlgorithmVariant.objects.update_or_create(code=v_code, defaults=v_defaults)
                seen_variant_codes.add(v_code)
                created_vars += int(v_created)
                updated_vars += int(not v_created)

        deleted_vars = 0
        if not no_clean:
            deleted_vars, _ = AlgorithmVariant.objects.exclude(code__in=seen_variant_codes).delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Sync complete.\n"
                f"- Algorithms: created={created_algos}, updated={updated_algos}\n"
                f"- Variants:   created={created_vars}, updated={updated_vars}, deleted={deleted_vars}"
            )
        )
