from django.shortcuts import render
from django.views.generic import DetailView
from frontend.models import Movie

class MovieView(DetailView):
    model = Movie
    template_name = "movie.html"
    slug_field = "slug"
    slug_url_kwarg = "title"


