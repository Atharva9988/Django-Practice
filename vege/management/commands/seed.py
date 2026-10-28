from django.core.management.base import BaseCommand

from vege.seed import run_all


class Command(BaseCommand):
    help = "Seed departments, subjects, students, marks and report cards"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10)

    def handle(self, *args, **options):
        run_all(options["count"])