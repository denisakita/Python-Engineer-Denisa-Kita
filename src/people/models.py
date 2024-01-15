from django.db import models


# SWAPI People Model

class SWAPIPeopleModel(models.Model):
    name = models.CharField(max_length=255)
    height = models.CharField(max_length=10)
    mass = models.CharField(max_length=10)
    hair_color = models.CharField(max_length=50)
    skin_color = models.CharField(max_length=50)
    eye_color = models.CharField(max_length=50)
    birth_year = models.CharField(max_length=10)
    gender = models.CharField(max_length=20)
    homeworld = models.URLField()
    url = models.URLField()
    date = models.DateTimeField()

    class Meta:
        app_label = 'people'
        verbose_name = 'SWAPIPerson'
        verbose_name_plural = 'SWAPIPeople'
        db_table = 'swapi_people'

    def __str__(self):
        return self.name
