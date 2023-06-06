import csv
import logging
import sys

import psycopg2
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(name)s, %(message)s',
)
handler.setFormatter(formatter)


class Command(BaseCommand):
    help = 'Импорт объектов в БД из CSV файлов'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help="Путь к файлу")

    def handle(self, *args, **options):
        file_path = options['path']
        conn = psycopg2.connect(
            'host=db port=5432 dbname=postgres '
            'user=postgres password=postgres')
        cur = conn.cursor()
        temp = []
        with open(file_path, encoding='utf8', mode='r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', )
            for row in reader:
                temp.append(row)
            cur.executemany(
                'INSERT INTO recipes_ingredient'
                '(name, measurement_unit) VALUES (%s, %s)', temp
            )
        conn.commit()
        conn.close()
        logger.info('How do you do')
