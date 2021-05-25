from django                     import template
# from django.contrib.auth.models import Group

register = template.Library()


#########################################################################
# {% if request.user|group_verify:"level_gpk level_brest" %} {% endif %}
#########################################################################
@register.filter(name='group_verify')
def group_verify(user, group_names):
    if user.is_superuser: return True
    ret = False
    for group_name in group_names.split():
        if user.groups.filter(name=group_name).exists():  # bool(user.groups.filter(name__in=group_name))
            ret = True
            break
    return ret


# @register.filter(name='group_verify')
# def group_verify(user, group_name):
#     group = Group.objects.filter(name=group_name)
#     if group:
#         group = group.first()
#         return group in user.groups.all()
#     else:
#         return False
