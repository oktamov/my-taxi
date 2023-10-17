import json

from django.conf import settings
from django.core.management.base import BaseCommand

from common.models import Country


class Command(BaseCommand):
    help = "create countries from json file"

    def handle(self, *args, **kwargs):
        with open(f"{settings.BASE_DIR}/common/management/commands/country_codes.json", "r") as f:
            countries_data = json.load(f)
            for country_data in countries_data:
                Country.objects.update_or_create(
                    code=country_data.get("code"),
                    defaults={
                        "name": country_data.get("name"),
                        "dial_code": country_data.get("dial_code"),
                    },
                )
        self.stdout.write(self.style.SUCCESS(f"Successfully {len(countries_data)} country added."))
