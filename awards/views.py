from django.shortcuts import render
from .models import Award


def display_awards(request):
    awards = Award.objects.all()
    return render(request, 'awards/awards.html', {'awards': awards})
