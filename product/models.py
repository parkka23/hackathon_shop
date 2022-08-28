from pydoc import describe
from django.db import models
from category.models import Category
from django.contrib.auth import get_user_model

# Create your models here.

User=get_user_model()

class Product(models.Model):

    title=models.CharField(max_length=100)
    description=models.TextField()
    owner=models.ForeignKey(User,related_name='products', on_delete=models.CASCADE)

    price=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    preview=models.ImageField(upload_to='images/', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['created_at']

    def __str__(self):
        return f'{self.owner} -> {self.title}'

class ProductImages(models.Model):
    title=models.CharField(max_length=150,blank=True)
    image=models.ImageField(upload_to='images/')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    @staticmethod
    def generate_name():
        from random import randint
        return 'image'+str(randint(100000,999999))

    def save(self,*args,**kwargs):
        self.title=self.generate_name()
        return super(ProductImages, self).save(*args,**kwargs)


class Comment(models.Model):
    owner=models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    product=models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.product} -> {self.created_at}'



class Like(models.Model):
    owner=models.ForeignKey(User, related_name='liked', on_delete=models.CASCADE)
    product=models.ForeignKey(Product, related_name='likes', on_delete=models.CASCADE)
    
    class Meta:
        unique_together=['product','owner']

class Favourites (models.Model):
    owner=models.ForeignKey(User, related_name='favourites', on_delete=models.CASCADE)
    product=models.ForeignKey(Product, related_name='favourites', on_delete=models.CASCADE)
    class Meta:
        unique_together=['product','owner']

