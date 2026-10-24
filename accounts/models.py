from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    user_bio = models.CharField(max_length=60)
    user_profile_image = models.ImageField(upload_to="profile")
    