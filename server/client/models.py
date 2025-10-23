from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )
    patronymic = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)

class Books(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=100)
    year = models.IntegerField()
    image = models.ImageField(upload_to='books/')
    genre = models.ManyToManyField(Genre)   