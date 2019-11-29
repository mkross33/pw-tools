def inactive_today(members):
    total = 0
    red = 0
    purple = 0
    for member in members:
        time_inactive = member.days_inactive()
        days_inactive_threshold = 3
        if time_inactive >= days_inactive_threshold:
            total += 1
            if member.activity_color() == 'red':
                red += 1
            else:
                purple += 1
    stats = {'total': total, 'red': red, 'purple': purple}
    return stats
