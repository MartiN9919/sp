from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from data_base_driver.constants.const_dat import DAT_OWNER_LINES, DAT_OWNER_REGIONS, DAT_OWNER_GROUPS, DAT_OWNER_USERS
from .models import ModelCustomUser, ModelOwnerGroups, ModelOwnerLines, ModelOwnerRegions

admin.site.unregister(Group)


@admin.register(ModelOwnerLines)
class ModelOwnerLinesAdmin(admin.ModelAdmin):
    list_display = (
        DAT_OWNER_LINES.TITLE,
        DAT_OWNER_LINES.PARENT_ID,
    )
    list_per_page = 20


@admin.register(ModelOwnerRegions)
class ModelOwnerRegionsAdmin(admin.ModelAdmin):
    list_display = (
        DAT_OWNER_REGIONS.TITLE,
        DAT_OWNER_REGIONS.PARENT_ID,
    )
    list_per_page = 20


@admin.register(ModelOwnerGroups)
class ModelOwnerGroupsAdmin(admin.ModelAdmin):
    list_display = (
        DAT_OWNER_GROUPS.TITLE,
        DAT_OWNER_GROUPS.OWNER_REGIONS,
        DAT_OWNER_GROUPS.OWNER_LINES,
        DAT_OWNER_GROUPS.DESCRIPT,
    )
    list_per_page = 20


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
