from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('MEMBER', 'Member'),
        ('OWNER', 'Workspace Owner'),
        ('ADMIN', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    banned = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username