from django.urls import path
from frontend.views import MovieView

urlpatterns = [
    path("<slug:title>/", MovieView.as_view(), name="movieview")
]
