from django.core.management import BaseCommand
from .extract_data_db import extract_data
import traceback


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-u', '--update', action='store_true', help='update database products')

    def handle(self, *args, **options):
        try:
            if options['update']:
                extract_data()

        except Exception as e:
            traceback.print_exc()
