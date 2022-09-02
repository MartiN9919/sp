from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from data_base_driver.constants.const_dat import DAT_OWNER_GROUPS, DAT_OWNER_USERS, \
    DAT_OWNER_GROUPS_REL
from .models import ModelCustomUser, ModelOwnerGroups, ModelOwnerGroupsRel

admin.site.unregister(Group)

@admin.register(ModelOwnerGroups)
class ModelOwnerGroupsAdmin(admin.ModelAdmin):
    list_display = (
        DAT_OWNER_GROUPS.ID,
        DAT_OWNER_GROUPS.TITLE,
        DAT_OWNER_GROUPS.OWNER_LINES_ID,
        DAT_OWNER_GROUPS.DESCRIPT,
    )
    list_editable = ('descript','title','owner_lines_id',)
    list_filter = (DAT_OWNER_GROUPS.OWNER_LINES_ID,)

    list_per_page = 20



@admin.register(ModelOwnerGroupsRel)
class ModelOwnerGroupsRelAdmin(admin.ModelAdmin):
    list_display = (
        DAT_OWNER_GROUPS_REL.ID,
        DAT_OWNER_GROUPS_REL.NODE_ID,
        DAT_OWNER_GROUPS_REL.PARENT_ID,
        DAT_OWNER_GROUPS_REL.READ_ONLY,
        DAT_OWNER_GROUPS_REL.DESCRIPT,


    )
    list_editable = ('parent_id','read_only','descript','node_id')
    list_filter = (DAT_OWNER_GROUPS_REL.READ_ONLY,)

@admin.register(ModelCustomUser)
class ModelCustomUserAdmin(UserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': (DAT_OWNER_USERS.USERNAME, DAT_OWNER_USERS.PASSWORD)}),
        (_('Personal info'), {'fields': (DAT_OWNER_USERS.FIRST_NAME, DAT_OWNER_USERS.LAST_NAME)}),
        (_('Permissions'), {
            'fields': (DAT_OWNER_USERS.IS_ACTIVE, DAT_OWNER_USERS.IS_STAFF, DAT_OWNER_USERS.IS_SUPERUSER,
                       DAT_OWNER_USERS.IS_WRITE, DAT_OWNER_USERS.OWNER_GROUPS, DAT_OWNER_USERS.USER_PERMISSION),
        }),
    )
    list_display = (
        DAT_OWNER_USERS.USERNAME,
        DAT_OWNER_USERS.FIRST_NAME,
        DAT_OWNER_USERS.LAST_NAME,
        DAT_OWNER_USERS.IS_STAFF,
        DAT_OWNER_USERS.OWNER_GROUPS
    )
    list_filter = (
        DAT_OWNER_USERS.IS_STAFF,
        DAT_OWNER_USERS.IS_SUPERUSER,
        DAT_OWNER_USERS.IS_ACTIVE,
        DAT_OWNER_USERS.OWNER_GROUPS
    )
    search_fields = (
        DAT_OWNER_USERS.USERNAME,
        DAT_OWNER_USERS.FIRST_NAME,
        DAT_OWNER_USERS.LAST_NAME
    )
    filter_horizontal = (DAT_OWNER_USERS.USER_PERMISSION,)
    list_per_page = 50
