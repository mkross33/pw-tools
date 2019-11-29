from django.db import models


class PwKey(models.Model):
    key = models.CharField(max_length=128)
    key_owner = models.CharField(max_length=64)
    alliance_officer = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    # has key has used up daily call limit
    limited = models.BooleanField(default=False)