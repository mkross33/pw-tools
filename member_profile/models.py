from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=64)
    # for using the profile name rather than current in-game ruler name, if the two are different
    override_ruler_name = models.BooleanField(default=False)
    joined_date = models.DateField(null=True, blank=True)
    nation_id = models.IntegerField(unique=True)

