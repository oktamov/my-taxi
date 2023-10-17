from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Country(models.Model):
    name = models.CharField(max_length=100)
    dial_code = models.CharField(max_length=15)
    code = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Region(MPTTModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions")
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
