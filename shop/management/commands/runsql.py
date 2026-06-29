from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Run SQL query (alternative to dbshell on Windows)'

    def add_arguments(self, parser):
        parser.add_argument('sql', nargs='?', default='.tables')

    def handle(self, *args, **options):
        sql = options['sql'].strip()

        if sql == '.tables':
            sql = (
                "SELECT name FROM sqlite_master "
                "WHERE type='table' ORDER BY name"
            )

        with connection.cursor() as cursor:
            cursor.execute(sql)

            if not cursor.description:
                self.stdout.write(self.style.SUCCESS('OK'))
                return

            columns = [col[0] for col in cursor.description]
            self.stdout.write(' | '.join(columns))
            self.stdout.write('-' * 40)

            for row in cursor.fetchall():
                self.stdout.write(' | '.join(str(value) for value in row))
