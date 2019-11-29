from django.shortcuts import render
from member_monitering.models import Member

def dashboard(request):
    members = Member.objects.filter(status='active', vm=False)
    inactives = inactive_today(members)
    war_count = len(Wars.objects.filter(active=True))
    vm_count = len(Member.objects.filter(vm=True))
    defcon = Defcon.objects.get(active=True).level
    users = User.objects.all()
    enemies = Enemy.objects.all()
    groups = Group.objects.all()
    context = {'activity': inactives, 'wars': war_count, 'vm_count': vm_count, 'defcon': defcon, 'users': users,
               'enemies': enemies, 'groups': groups}
    return render(request, 'member_monitering/dashboard.html', context)


def update_group(request):
    user_id = request.POST['user']
    group_id = request.POST['group']
    operation = request.POST['operation']
    user = User.objects.get(id=user_id)
    group = Group.objects.get(id=group_id)
    if operation == 'add':
        group.user_set.add(user)
    else:
        group.user_set.remove(user)
    return HttpResponseRedirect(reverse("dashboard"))


def change_defcon(request):
    level = request.POST['defcon']
    current = Defcon.objects.get(active=True)
    if current.level != level:
        current.active = False
        current.save()
        new = Defcon.objects.get(level=level)
        new.active = True
        new.save()
    return HttpResponseRedirect(reverse("dashboard"))


def update_enemies(request):
    if request.POST.get('remove', False):
        enemy = EnemyAlliance.objects.get(alliance_id=request.POST['remove']).delete()
    if request.POST.get('add', False):
        if not EnemyAlliance.objects.filter(alliance_id=request.POST['add']).exists():
            alliance = pw_api(api='alliance', object_id=request.POST['add'])
            if 'error' in alliance:
                return error(request, 'That was not a valid alliance ID')
            new_enemy = EnemyAlliance(alliance_id=request.POST['add'], alliance_name=alliance['name'])
            new_enemy.save()
    # redirect back to the Dashboard
    return HttpResponseRedirect(reverse("dashboard"))
