from ast import arg
from django.db import models
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    slug = models.SlugField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description=models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
