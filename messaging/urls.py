from django.urls import path
from . import views

urlpatterns = [
    path('settings', views.settings, name="messaging-settings"),
    path('add_messenger', views.add_messenger, name="messaging-add-messenger"),
    path('remove_messenger', views.remove_messenger, name='messaging-remove-messenger'),
    path('set_active_messenger', views.set_active_messenger, name='messaging-set-active-messenger'),
    path('set_message', views.set_message, name='messaging-set-message'),
    ]
