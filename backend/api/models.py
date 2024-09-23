from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    github_token = models.CharField(max_length=255, blank=True, null=True)
    selected_repository = models.CharField(max_length=255, blank=True, null=True)
    github_username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username