from django.db import models


class ColorBlocks(models.IntegerChoices):
    AQUA = 1, "Aqua"
    BLACK = 2, "Black"
    BLUE = 3, "Blue"
    BROWN = 4, "Brown"
    GREEN = 5, "Green"
    LIME = 6, "Lime"
    MAROON = 7, "Maroon"
    OLIVE = 8, "Olive"
    ORANGE = 9, "Orange"
    PINK = 10, "Pink"
    PURPLE = 11, "Purple"
    RED = 12, "Red"
    WHITE = 13, "White"
    YELLOW = 14, "Yellow"
    GRAY = 15, "Gray"
    BEIGE = 16, "Beige"


class AlliancePositions(models.IntegerChoices):
    LEADER = 5
    HEIR = 4
    OFFICER = 3
    MEMBER = 2
    APPLICANT = 1


class WarPolicy(models.IntegerChoices):
    ATTRITION = 1
    TURTLE = 2
    BLITZKRIEG = 3
    FORTRESS = 4
    MONEYBAGS = 5, "MoneyBags"
    PIRATE = 6
    TACTICIAN = 7
    GUARDIAN = 8
    COVERT = 9
    ARCANE = 10


class DomesticPolicy(models.IntegerChoices):
    MANIFEST_DESTINY = 1
    OPEN_MARKETS = 2
    TECHNOLOGICAL_ADVANCEMENT = 3
    IMPERIALISM = 4
    URBANIZATION = 5


class Continents(models.TextChoices):
    NORTH_AMERICA = "North America"
    SOUTH_AMERICA = "South America"
    AFRICA = "Africa"
    EUROPE = "Europe"
    ASIA = "Asia"
    AUSTRALIA = "Australia"
    ANTARCTICA = "Antarctica"
