from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

class User(AbstractUser):
    emp_id = models.CharField(max_length=15,null=True)
    email = models.EmailField(null=True)
    class Meta:
        db_table = "users"
    def __str__(self):
        return self.email

