from django.db import models


# SWAPI Collection Model

class SWAPICollectionDataset(models.Model):
    filename = models.CharField(max_length=255)
    download_date = models.DateTimeField()

    class Meta:
        app_label = 'core'
        verbose_name = 'SWAPICollection'
        verbose_name_plural = 'SWAPICollections'
        db_table = 'swapi_collections'

    def __str__(self):
        return self.filename
