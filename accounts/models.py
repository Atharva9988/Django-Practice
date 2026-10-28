from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    user_bio = models.CharField(max_length=60, blank=True)
    user_profile_image = models.ImageField(upload_to="profile", blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()