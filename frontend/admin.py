from django.contrib import admin
from frontend.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass
