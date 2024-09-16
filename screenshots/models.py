import datetime

from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix
from minio import Minio

from videoshotsPureDjango import settings


# Create your models here.

class Screenshot(models.Model):
    screenshot = models.FileField(verbose_name="Bild",
                            storage=MinioBackend(bucket_name='videoshotsdjango'),
                            upload_to=iso_date_prefix)

    title = models.CharField(max_length=70, verbose_name="Titel")
    description = models.TextField(max_length=300, verbose_name="Beschreibung")
    publication_date = models.DateField(default=datetime.datetime.now().strftime("%Y-%m-%d"))

    def get_queryset(self):
        return Screenshot.objects.all()

    def get_url(self):
        return self.screenshot.url
