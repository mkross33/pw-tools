from django.db import models
from django.utils import timezone


class Member(models.Model):
    nation_id = models.IntegerField(primary_key=True)
    ruler = models.CharField(max_length=64)
    nation = models.CharField(max_length=64)
    retired = models.BooleanField(default=False)
    vacation_mode = models.BooleanField(default=False)

    def days_inactive(self):
        time = self.logs.latest('timestamp')
        daily_minutes = 1440
        days = time.time_inactive / daily_minutes
        return round(days, 1)

    # determines the in-game color code for the users activity level
    def activity_color(self):
        # As of PW update 1.2.4, all vacation mode players are now assigned to grey
        if self.vacation_mode:
            return 'grey'
        time = self.logs.latest('timestamp')
        red_minutes = 4320
        purple_minutes = 10080
        if time.time_inactive >= purple_minutes:
            return 'purple'
        elif time.time_inactive >= red_minutes:
            return 'red'
        # yellow / blue (online now / last 1 hour) are not tracked and treated as green (online past 24h)
        else:
            return 'green'

    def get_log_value(self, field):
        data = self.logs.latest('timestamp')
        value = getattr(data, field)
        return value


class MemberLog(models.Model):
    nation_id = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='logs')
    # Though we mainly care about days, for consistency the logs mirror the game API in measuring activity in minutes
    minutes_inactive = models.IntegerField()
    color = models.CharField(max_length=64)
    soldiers = models.IntegerField()
    tanks = models.IntegerField()
    aircraft = models.IntegerField()
    ships = models.IntegerField()
    spies = models.IntegerField()
    money = models.FloatField()
    gasoline = models.FloatField()
    munitions = models.FloatField()
    steel = models.FloatField()
    aluminum = models.FloatField()
    uranium = models.FloatField()
    active_wars = models.IntegerField()
    cities = models.SmallIntegerField()
    score = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)


# Defcon levels and their associated mandatory military minimums.
class Defcon(models.Model):
    level = models.SmallIntegerField(primary_key=True)
    # units required per city (total = requirement * number of cities)
    soldiers = models.IntegerField()
    tanks = models.IntegerField()
    aircraft = models.IntegerField()
    ships = models.IntegerField()
    spies = models.IntegerField()
    money = models.IntegerField()
    uranium = models.IntegerField()
    gasoline = models.IntegerField()
    munitions = models.IntegerField()
    aluminum = models.IntegerField()
    steel = models.IntegerField()
    active = models.BooleanField(default=False)
