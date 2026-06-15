from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class Photo(models.Model):
    image = ThumbnailerImageField(upload_to="photos")

    class Meta:
        app_label = "tests"
