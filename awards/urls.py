from django.urls import path

from .views import display_awards

urlpatterns = [
    path('awards', display_awards, name='display-awards'),
]