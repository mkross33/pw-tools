from django.shortcuts import render


def member_view(request, member_id):
    member = Member.objects.get(nation_id=member_id)
    defcon = Defcon.objects.get(active=True)
    comparisons = ['soldiers', 'tanks', 'aircraft', 'ships', 'spies', 'money', 'uranium', 'gasoline',
                   'munitions', 'aluminum', 'steel']
    stats = MemberLog.objects.filter(member_id=member.nation_id).latest('timestamp')
    return render(request, 'profiles/profile.html', {'member': member,  'defcon': defcon,
                                                             'comparisons': comparisons, 'stats': stats})

