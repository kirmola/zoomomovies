import requests
import gzip
import json
from io import BytesIO
from datetime import datetime, timedelta

MOVIE_EXPORT_URL = "https://files.tmdb.org/p/exports/movie_ids_{month}_{day}_{year}.json.gz"
TV_EXPORT_URL = "https://files.tmdb.org/p/exports/tv_series_ids_{month}_{day}_{year}.json.gz"

def get_export_urls():
    today = datetime.utcnow() - timedelta(days=1)
    date_str = {
        "month": str(today.month).zfill(2),
        "day": str(today.day).zfill(2),
        "year": today.year
    }
    return (
        MOVIE_EXPORT_URL.format(**date_str),
        TV_EXPORT_URL.format(**date_str)
    )

def fetch_ids(export_url):
    print(f"📥 Downloading TMDB export from: {export_url}")
    resp = requests.get(export_url)
    if resp.status_code != 200:
        print(f"❌ Failed to download export from {export_url}")
        return []

    ids = []
    with gzip.GzipFile(fileobj=BytesIO(resp.content)) as f:
        for line in f:
            try:
                data = json.loads(line)
                ids.append(data["id"])
            except Exception:
                continue
    return ids

def save_ids_to_file(ids, filename):
    with open(filename, "w") as f:
        for _id in ids:
            f.write(f"{_id}\n")
    print(f"✅ {len(ids)} IDs saved to {filename}")

if __name__ == "__main__":
    movie_url, tv_url = get_export_urls()

    movie_ids = fetch_ids(movie_url)
    tv_ids = fetch_ids(tv_url)

    save_ids_to_file(movie_ids, "movie_ids.txt")
    save_ids_to_file(tv_ids, "tv_ids.txt")
