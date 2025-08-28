import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

