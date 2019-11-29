# custom template filters
from django import template

register = template.Library()

# register the filter
@register.filter(name='in_group')
# filter to check if a user has a specific member group by name
def in_group(user, group):
    return user.groups.filter(name=group).exists()


# Return a given field value from a members most recent log. Queries member class function.
@register.filter(name='member_value')
def member_value(member, field):
    return member.get_log_value(field)


# return the value of a field from a given object.
@register.filter(name='object_value')
def object_value(obj, field):
    return getattr(obj, field)
