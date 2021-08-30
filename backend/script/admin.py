from django.contrib import admin
from .models import ModelScript, ModelTrigger

from data_base_driver.constants.const_admin import PROJECT_TITLE_ADMIN
from data_base_driver.constants.const_dat import DAT_SYS_SCRIPT, DAT_SYS_TRIGGER

admin.site.site_header = PROJECT_TITLE_ADMIN


@admin.register(ModelScript)
class ModelScriptAdmin(admin.ModelAdmin):
    list_display = (
        'get_parent',
        DAT_SYS_SCRIPT.TITLE,
        DAT_SYS_SCRIPT.DESCRIPT,
        'get_owner',
        DAT_SYS_SCRIPT.ENEBLED,
        DAT_SYS_SCRIPT.TYPE,
    )

    ordering = (
        DAT_SYS_SCRIPT.TITLE,
        DAT_SYS_SCRIPT.TYPE,
    )

    list_editable = (
        DAT_SYS_SCRIPT.ENEBLED,
    )

    list_display_links = [
        DAT_SYS_SCRIPT.TITLE,
    ]

    fieldsets = (
        (None,
         {'fields':
             (
                 DAT_SYS_SCRIPT.TITLE,
                 DAT_SYS_SCRIPT.HINT,
                 (
                     DAT_SYS_SCRIPT.PARENT_ID,
                     DAT_SYS_SCRIPT.ICON,
                 ),
                 DAT_SYS_SCRIPT.CONTENT,
                 DAT_SYS_SCRIPT.DESCRIPT,
                 DAT_SYS_SCRIPT.VARIABLES,
                 (
                     DAT_SYS_SCRIPT.OWNER_LINE,
                     DAT_SYS_SCRIPT.ENEBLED,
                     DAT_SYS_SCRIPT.TYPE,
                 )
             )
         }),
    )

    list_per_page = 20

    @admin.display(description='Группа владельцев')
    def get_owner(self, obj):
        """
        Функция, взвращающая тип пользователя
        """
        return obj.owner

    @admin.display(description='Родительский id')
    def get_parent(self, obj):
        """
        Функция, взвращающая родительскую папку
        """
        return obj.parent


@admin.register(ModelTrigger)
class ModelTriggerAdmin(admin.ModelAdmin):
    list_display = (
        'get_object_title',
        DAT_SYS_TRIGGER.TITLE,
    )

    @admin.display(description='объект')
    def get_object_title(self, obj):
        return obj.object