from django.urls import path
from . import views

urlpatterns = [
    path('settings', views.settings, name="pwapi-settings"),
    path('add_key', views.add_key, name="pwapi-add-key"),
    path('remove_key', views.remove_key, name='pwapi-remove-key')
    ]
