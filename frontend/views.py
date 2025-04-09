from django.shortcuts import render
from django.views.generic import DetailView, ListView
from frontend.models import Movie

class MovieView(DetailView):
    model = Movie
    template_name = "movie.html"
    slug_field = "slug"
    slug_url_kwarg = "title"
    context_object_name = "movie"
    



class HomeView(ListView):
    model = Movie
    template_name = "index.html"
    context_object_name = "movies"
    

    def get_queryset(self):
        return super().get_queryset()[:10]
    
    
