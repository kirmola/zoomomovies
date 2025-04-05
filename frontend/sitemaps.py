from django.contrib.sitemaps import Sitemap
from frontend.models import (
    Movie
)

class MovieSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    limit = 50000


    def items(self):
        return Movie.objects.all()