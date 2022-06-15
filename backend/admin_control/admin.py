from django.contrib import admin
from admin_control.models import ModelNotification, Manual
from data_base_driver.constants.const_dat import DAT_SYS_NOTIFY, DAT_SYS_MANUAL


@admin.register(ModelNotification)
class ModelNotificationAdmin(admin.ModelAdmin):
    list_display = (
        DAT_SYS_NOTIFY.TYPE,
        'return_from_user',
        'return_to_user',
    )

    fieldsets = (
        (None,
         {'fields':
             (
                 DAT_SYS_NOTIFY.FROM_USER,
                 DAT_SYS_NOTIFY.TO_USER,
                 DAT_SYS_NOTIFY.TYPE,
                 DAT_SYS_NOTIFY.CONTENT,
                 DAT_SYS_NOTIFY.FILE,
             )
         }),
    )

    list_filter = (DAT_SYS_NOTIFY.TYPE,)
    list_per_page = 20

    @admin.display(description='От кого')
    def return_from_user(self, object):
        return object.from_user

    @admin.display(description='Кому')
    def return_to_user(self, object):
        return object.to_user


@admin.register(Manual)
class ModelManual(admin.ModelAdmin):
    list_display = (
        DAT_SYS_MANUAL.TITLE,
        DAT_SYS_MANUAL.UPDATE_DATETIME,
    )
    fieldsets = (
        (None, {'fields': (DAT_SYS_MANUAL.TITLE, DAT_SYS_MANUAL.FILE,)}),
    )
    ordering = (DAT_SYS_MANUAL.TITLE,)
