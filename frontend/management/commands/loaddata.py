import json
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from frontend.models import Movie
from tqdm import tqdm
from shortuuid import ShortUUID


class Command(BaseCommand):
    help = "Load movies and TV series from tmdb.jsonl into the Movie model."

    def handle(self, *args, **kwargs):
        tmdb_path = Path("/home/kirmola/Downloads/tmdb.jsonl")

        if not tmdb_path.exists():
            self.stderr.write("tmdb.jsonl not found.")
            return

        self.load_data(tmdb_path)

    def load_data(self, path):
        self.stdout.write(f"Loading data from {path.name}...")

        with path.open("r", encoding="utf-8") as f:
            objects = []
            seen_slugs = set(Movie.objects.values_list("slug", flat=True))  # Get existing slugs

            for line in tqdm(f, desc="TMDB"):
                try:
                    data = json.loads(line)
                    is_tv = data.get("type") == "tv"

                    title = data["name"] if is_tv else data["title"]
                    original_title = data.get("original_name") if is_tv else data.get("original_title", "")
                    release_field = "first_air_date" if is_tv else "release_date"
                    release_date = self.parse_date(data.get(release_field))
                    year = release_date.year if release_date else ""

                    imdb_id = data.get("imdb_id")
                    tmdb_id = data.get("tmdb_id")

                    # === Slug generation ===
                    base_slug = slugify(f"{title}-{year}")
                    slug = base_slug
                    if slug in seen_slugs:
                        if imdb_id:
                            slug = slugify(f"{title}-{year}-{imdb_id}")
                        elif tmdb_id:
                            slug = slugify(f"{title}-{year}-{tmdb_id}")
                        else:
                            slug = slugify(f"{title}-{year}-{ShortUUID().random(8)}")

                        # Last-resort fallback in case it still exists
                        while slug in seen_slugs:
                            slug = slugify(f"{title}-{year}-{ShortUUID().random(8)}")

                    seen_slugs.add(slug)

                    obj = Movie(
                        tmdb_id=tmdb_id,
                        imdb_id=imdb_id,
                        title=title,
                        original_title=original_title,
                        description=data.get("overview") or data.get("description", ""),
                        tagline=data.get("tagline", ""),
                        rating=data.get("vote_average") or data.get("rating"),
                        vote_count=data.get("vote_count", 0),
                        popularity=data.get("popularity"),
                        release_date=release_date,
                        genres=data.get("genres", []),
                        spoken_languages=data.get("spoken_languages", []),
                        poster_path=data.get("poster_path", ""),
                        backdrop_path=data.get("backdrop_path", ""),
                        adult=data.get("adult", False),
                        extra_images=data.get("extra_images", []),
                        downlinks=data.get("downlinks", []),
                        slug=slug,
                        type=data.get("type"),
                        fileid=data.get("fileid", "")
                    )
                    objects.append(obj)
                except Exception as e:
                    self.stderr.write(f"Error parsing entry: {e}")

        # Save in batches
        BATCH_SIZE = 25000
        with transaction.atomic():
            for i in tqdm(range(0, len(objects), BATCH_SIZE), desc="Saving"):
                Movie.objects.bulk_create(objects[i:i + BATCH_SIZE])

        self.stdout.write(f"Imported {len(objects)} entries.")

    @staticmethod
    def parse_date(date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None
