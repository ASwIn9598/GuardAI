from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
import os
from django.core.files.base import ContentFile
from django.utils.timezone import now
from datetime import datetime   

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom user model
class User(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    username = None  
    email = models.EmailField(unique=True)  

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  


class AnalyzedVideo(models.Model):
    video_file = models.FileField(upload_to="videos/")  # Stores the video file
    analysis_result = models.BooleanField(null=True, blank=True)  # True: Knife detected, False: No knife, None: Not analyzed
    analyzed_at = models.DateTimeField(auto_now_add=True)  # Timestamp of analysis

    def __str__(self):
        return f"Video {self.id}: {'Knife detected' if self.analysis_result else 'No knife'}"
    

class RecordedVideo(models.Model):
    name = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='recorded_videos/')
    created_at = models.DateTimeField(default=datetime.now, blank=True) #made changes auto_now_add=True as parameter


    def __str__(self):
        return self.name