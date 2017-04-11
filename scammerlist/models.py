from django.db import models

# Create your models here.


class Catalog(models.Model):
    type_cat = models.CharField(max_length=200)

    def __str__(self):
        return self.type_cat

class Person(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=10)
    detail = models.CharField(max_length=400)

    def __str__(self):
        return self.name

