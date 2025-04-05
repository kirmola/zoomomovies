from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.urls import reverse
# Create your models here.

class Movie(models.Model):

    title = models.CharField(_("movie title"), max_length=255)
    description = models.TextField(_("description"))
    slug = AutoSlugField(populate_from="title", unique=True)
    downlinks = models.JSONField(_("download links"), default=list)

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Movie_detail", kwargs={"pk": self.pk})
