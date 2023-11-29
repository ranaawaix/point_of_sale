from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group


# Create your models here.


GROUP_CHOICES = [
    ('A', 'Admin'),
    ('S', 'Staff'),
]
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]
STATUS_CHOICES = [
    ('Active', 'Active'),
    ('In-Active', 'In-Active'),
]


class User(AbstractUser):
    group = models.CharField(choices=GROUP_CHOICES, max_length=250, default='S', null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=250, default='M', null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=250, default='Active', null=True, blank=True)

    def __str__(self):
        return f'{self.id}-{self.username}'


class Groups(Group):
    class Meta:
        proxy = True
        verbose_name_plural = 'Groups'
