from django.db import models
from member_profile.models import Profile
from .constants import MINUTES_PER_DAY, MINUTES_PER_HOUR
from django.utils import timezone
from .enums import AlliancePositions, ColorBlocks, WarPolicy, DomesticPolicy, Continents


class Nation(models.Model):
    minutes_inactive = models.IntegerField()
    color = models.IntegerField(choices=ColorBlocks.choices, default=ColorBlocks.GRAY)
    alliance_position = models.IntegerField(choices=AlliancePositions.choices, default=AlliancePositions.APPLICANT)
    offensive_war_count = models.IntegerField()
    defensive_war_count = models.IntegerField()
    score = models.FloatField()
    turns_in_vm = models.IntegerField()
    infrastructure = models.FloatField()
    soldiers = models.IntegerField()
    tanks = models.IntegerField()
    aircraft = models.IntegerField()
    ships = models.IntegerField()
    war_policy = models.IntegerField(choices=WarPolicy.choices)
    domestic_policy = models.IntegerField(choices=DomesticPolicy.choices)
    continent = models.TextField(choices=Continents.choices)
    city_count = models.IntegerField()

    def string_time_inactive(self):
        """
        Generate a formatted string representation of the time a user has been inactive.
        :return: a simple string timestamp for days hours and minutes
        """
        days = self.minutes_inactive / MINUTES_PER_DAY
        leftover_minutes = days % MINUTES_PER_DAY
        hours = leftover_minutes / MINUTES_PER_HOUR
        minutes = self.minutes_inactive - (days * MINUTES_PER_DAY) - (hours * MINUTES_PER_HOUR)
        return f"{days} days {hours} hours and {minutes} minutes."

    class Meta:
        abstract = True


class Member(Nation):
    member_id = models.ForeignKey(Profile, to_field="nation_id", db_column="nation_id", on_delete=models.CASCADE, related_name='logs')
    spies = models.IntegerField()
    money = models.FloatField()
    gasoline = models.FloatField()
    munitions = models.FloatField()
    steel = models.FloatField()
    aluminum = models.FloatField()
    uranium = models.FloatField()
    food = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    # determines the in-game color code for the users activity level
    def activity_color(self):
        orange_threshold = MINUTES_PER_DAY
        red_threshold = MINUTES_PER_DAY * 3
        purple_threshold = MINUTES_PER_DAY * 7
        if self.minutes_inactive >= purple_threshold:
            return 'purple'
        elif self.minutes_inactive >= red_threshold:
            return 'red'
        elif self.minutes_inactive >= orange_threshold:
            return 'orange'
        # Blue (online last hour) and green (online now) are not tracked and treated in the app as yellow (online today)
        else:
            return 'yellow'
