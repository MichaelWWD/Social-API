from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    # Note: handle DOB,  full name & user type/ membership 
    email = models.EmailField(unique=True, blank=False, null=False)

