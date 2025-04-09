from django.test import TestCase
from django.urls import reverse
from frontend.models import Movie

class MovieViewURLTest(TestCase):
    def setUp(self):
        # If your test DB needs seed data, add here or use fixtures
        pass

    def test_movie_view_urls_return_200(self):
        movies = Movie.objects.all()
        for movie in movies:
            url = reverse("movieview", kwargs={"title": movie.slug})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed for slug: {movie.slug}")
