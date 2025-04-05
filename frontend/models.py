from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.urls import reverse
# Create your models here.

class Movie(models.Model):

    title = models.CharField(_("movie title"), max_length=255, db_index=True)
    description = models.TextField(_("description"))
    slug = AutoSlugField(populate_from="title", unique=True, unique_with=["title", "fileid"])
    downlinks = models.JSONField(_("download links"), default=list)
    fileid = models.CharField(_("terabox file id"), max_length=50)

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movieview", kwargs={"title": self.slug})
