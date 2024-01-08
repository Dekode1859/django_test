# dat/models.py

from django.db import models

class DataEntry(models.Model):
    # name = models.CharField(max_length=255)
    url = models.URLField()
    class Meta:
        app_label = 'dat'
