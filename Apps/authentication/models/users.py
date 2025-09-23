from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True) 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        self.clean
        super().save(*args, **kwargs)