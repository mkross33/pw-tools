from django.db import models


class PwKey(models.Model):
    key = models.CharField(max_length=128)
    owning_nation_id = models.IntegerField()
    owning_ruler_name = models.CharField(max_length=64)
    officer_permissions = models.BooleanField(default=False)
    rate_limited = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
