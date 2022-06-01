from django.core.management.base import BaseCommand

import csv
from colorama import init, Fore

from app.models import Ingredient

init(autoreset=True)


class Command(BaseCommand):
    """Management-команда наполняющей базу данных тестовыми данными
    из каталога /data/.
    """
    help = ('Helps to fill the database with test '
            'data from "/data"')

    def fill_table_ingredient(self):
        self.stdout.write(
            '  Applying /data/ingredients.csv', ending='... '
        )
        try:
            with open(
                './data/ingredients.csv', encoding='utf-8'
            ) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for __, row in enumerate(reader):
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
            return self.stdout.write(Fore.GREEN + 'OK')
        except Exception as error:
            self.stderr.write(Fore.RED + 'FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def handle(self, *args, **options):
        self.stdout.write(
            'Operations to perform:\n'
        )
        try:
            self.fill_table_ingredient()
        except Exception as error:
            self.stderr.write(
                Fore.RED + f'Execution error - {error}!'
            )
