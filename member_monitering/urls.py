from django.urls import path
from . import views

urlpatterns = [
    path('activity', views.activity, name="member-monitering-activity"),
    path('members_list', views.members_list, name='member-monitering-members-list'),
    path('inactivity_warning', views.inactivity_warning, name='member-monitering-inactivity-warning'),
    ]
