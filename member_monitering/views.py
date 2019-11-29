from django.shortcuts import render
from .models import Member, Defcon, MemberLog
from .utils import inactive_today
from messaging.models import Message, Messenger
from django.http import HttpResponseRedirect
from django.urls import reverse


def activity(request):
    active_members = Member.objects.filter(retired=False, vm=False)
    activity_stats = inactive_today(active_members)
    return render(request, 'member_monitering/activity.html', {'members': active_members, 'activity_stats': activity_stats})


def inactivity_warning(request):
    recipient_id = request.POST['recipient']
    recipient = Member.objects.get(nation_id=recipient_id)
    contact = {'leader': recipient.ruler, 'nation': recipient.nation, 'nationid': recipient.nation_id}
    messenger = Messenger.objects.get(active=True)
    message = Message.objects.get(category='activity')
    message.send(contact, messenger)
    message.log(contact, messenger)
    return HttpResponseRedirect(reverse('member-monitering-activity'))


def members_list(request):
    member_list = Member.objects.filter(retired=False)
    return render(request, 'member_monitering/members_list.html', {'members': member_list})


