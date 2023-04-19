from time import sleep
from django.core.management.base import BaseCommand

from django.db.utils import OperationalError

from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("\nWaiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    self.style.WARNING("Dabase unavailable, waiting 1 second...")
                )
                sleep(1)
        self.stdout.write(self.style.HTTP_INFO("Database available."))
        self.stdout.write(self.style.SUCCESS("Connection success."))
