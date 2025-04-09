from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.urls import reverse
# Create your models here.

class Movie(models.Model):

    
    tmdb_id = models.IntegerField(db_index=True, null=True)
    imdb_id = models.CharField(max_length=15, blank=True, null=True)
    title = models.CharField(_("movie title"), max_length=255, db_index=True)
    original_title = models.CharField(max_length=255, blank=True, db_index=True, null=True)
    description = models.TextField(_("description"), blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(_("rating"), null=True, blank=True)
    vote_count = models.IntegerField(default=0, null=True)
    popularity = models.FloatField(null=True, blank=True)
    release_date = models.DateField(blank=True, null=True)
    genres = models.JSONField(default=list)
    spoken_languages = models.JSONField(default=list)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    adult = models.BooleanField(default=False)
    type = models.CharField(_("type"), max_length=50, null=False)
    similar_movies = models.ManyToManyField("self", blank=True)
    extra_images = models.JSONField(default=list)  # posters/backdrops list

    # Your original fields
    slug = models.CharField(_("slug"), max_length=100)
    downlinks = models.JSONField(_("download links"), default=list)
    fileid = models.CharField(_("terabox file id"), max_length=50)
    created = models.DateTimeField(_("created on"), auto_now_add=True)
    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movieview", kwargs={"title": self.slug})
