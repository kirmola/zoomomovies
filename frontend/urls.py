from django.urls import path
from frontend.views import MovieView, HomeView, SearchView

urlpatterns = [
    path("", HomeView.as_view(), name="homeview"),
    path("<slug:title>/", MovieView.as_view(), name="movieview"),
    path("search/all/", SearchView.as_view(), name="search")
]
