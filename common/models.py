from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Country(models.Model):
    name = models.CharField(max_length=100)
    dial_code = models.CharField(max_length=15)
    code = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
