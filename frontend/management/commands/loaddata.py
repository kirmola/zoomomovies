import json
from django.core.management.base import BaseCommand
from frontend.models import Movie
from django.conf import settings


class Command(BaseCommand):
    help = 'Bulk load files from files.jsonl into the database'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR /'files.jsonl'
        to_create = []
        existing_ids = set(Movie.objects.values_list('fileid', flat=True))
        total = 0
        skipped = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        title = data.get('title')
                        fileid = data.get('id')

                        if not title or not fileid:
                            continue

                        if fileid in existing_ids:
                            skipped += 1
                            continue

                        obj = Movie(title=title, fileid=fileid)
                        to_create.append(obj)
                        total += 1

                    except json.JSONDecodeError as e:
                        self.stderr.write(f"Invalid JSON line: {e}")
                    except Exception as e:
                        self.stderr.write(f"Error: {e}")

            if to_create:
                Movie.objects.bulk_create(to_create, batch_size=1000)

            self.stdout.write(self.style.SUCCESS(
                f"Import complete. Created: {total}, Skipped (duplicates): {skipped}"
            ))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
