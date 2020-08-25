from django.db import models
from member_profile.models import Profile


class AwardCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)


class Award(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/awards/')
    recipients = models.ManyToManyField(Profile)

