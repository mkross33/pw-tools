from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import MessageLog, Message, Messenger


def settings(request):
    messengers = Messenger.objects.all()
    if Messenger.objects.filter(active=True).exists():
        active_messenger = Messenger.objects.get(active=True)
    else:
        active_messenger = False
    if Message.objects.filter(category='recruitment').exists():
        recruitment = Message.objects.filter(category='recruitment')[0]
    else:
        recruitment = False
    if Message.objects.filter(category='activity').exists():
        activity = Message.objects.filter(category='activity')[0]
    else:
        activity = False
    context = {'messengers': messengers, 'active_messenger': active_messenger, 'recruitment': recruitment,
               'activity': activity}
    return render(request, 'messaging/settings.html', context)


def add_messenger(request):
    new_messenger = Messenger(ruler_name=request.POST['ruler'], username=request.POST['username'],
                              password=request.POST['password'])
    new_messenger.save()
    return HttpResponseRedirect(reverse('messaging-settings'))


def remove_messenger(request):
    messenger = Messenger.objects.get(id=request.POST['messenger'])
    messenger.delete()
    return HttpResponseRedirect(reverse('messaging-settings'))


def set_active_messenger(request):
    if Messenger.objects.filter(active=True).exists():
        current_active = Messenger.objects.get(active=True)
        current_active.active = False
        current_active.save()
    new_active = Messenger.objects.get(id=request.POST['messenger'])
    new_active.active = True
    new_active.save()
    return HttpResponseRedirect(reverse('messaging-settings'))


def set_message(request):
    msg_type = request.POST['type']
    subject = request.POST['subject']
    body = request.POST['body']

    current_message = Message.objects.filter(category=msg_type)
    if current_message.exists():
        current_message = current_message[0]
        current_message.subject = subject
        current_message.body = body
        current_message.save()
    else:
        new = Message(category=msg_type, subject=subject, body=body)
        new.save()

    return HttpResponseRedirect(reverse("messaging-settings"))

