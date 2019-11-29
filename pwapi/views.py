from django.shortcuts import render
from .models import PwKey
from django.http import HttpResponseRedirect
from django.urls import reverse


def settings(request):
    """ Handles requests for pwapi/settings
        View for displaying and managing PW API Keys"""

    pw_api_keys = PwKey.objects.all()
    return render(request, 'pwapi/pwapi.html', {'keys': pw_api_keys})


def add_key(request):
    if request.POST['officer_status'] == 'member':
        officer = False
    else:
        officer = True
    new_key = PwKey(key=request.POST['key'], key_owner=request.POST['owner'],
                    alliance_officer=officer)
    new_key.save()
    success_message = 'New API key added successfully'
    return HttpResponseRedirect(reverse('pwapi-settings'))


def remove_key(request):
    key = PwKey.objects.get(key=request.POST['key'])
    key.delete()
    return HttpResponseRedirect(reverse('pwapi-settings'))


