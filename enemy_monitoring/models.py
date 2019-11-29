from member_monitering.models import Member, MemberLog
from django.db import models
from django.utils import timezone


class EnemyAlliance(models.Model):
    alliance_id = models.IntegerField(primary_key=True)
    alliance_name = models.CharField(max_length=64)


class EnemyNation(models.Model):
    alliance = models.ForeignKey(EnemyAlliance, on_delete=models.CASCADE, related_name='nations')
    nation_id = models.IntegerField(primary_key=True)
    ruler = models.CharField(max_length=64)
    nation = models.CharField(max_length=64)
    score = models.FloatField()
    spies = models.IntegerField(default=9999)
    spy_slots = models.BooleanField(default=True)
    soldiers = models.IntegerField(default=9999)
    tanks = models.IntegerField(default=9999)
    aircraft = models.IntegerField(default=9999)
    ships = models.SmallIntegerField(default=9999)
    war_policy = models.CharField(max_length=64)
    war_slots = models.SmallIntegerField(default=9999)
    beige_turns = models.SmallIntegerField(default=9999)
    date = models.DateTimeField(default=timezone.now)


