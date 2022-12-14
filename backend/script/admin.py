from django.contrib import admin
from django_monaco_editor.widgets import AdminMonacoEditorWidget
from django import forms
from script.models import ModelScript, ModelTrigger, ModelScriptVariable, ModelTriggerVariable
from data_base_driver.constants.const_admin import PROJECT_TITLE_ADMIN
from data_base_driver.constants.const_dat import DAT_SYS_SCRIPT, DAT_SYS_TRIGGER

admin.site.site_header = PROJECT_TITLE_ADMIN


class ModelScriptVariableAdmin(admin.StackedInline):
    model = ModelScriptVariable

    fieldsets = (
        (None, {'fields': (('name', 'title', 'hint'),('type', 'list', 'obj'), ('necessary',))}),
    )


class ModelScriptForm(forms.ModelForm):
    class Meta:
        model = ModelScript
        fields = '__all__'
        widgets = {
            'content': AdminMonacoEditorWidget
        }


def delete_scripts(modeladmin, request, queryset):
    for script in queryset:
        script.delete()


delete_scripts.short_description = "Удалить выбранные Скрипты"


@admin.register(ModelScript)
class ModelScriptAdmin(admin.ModelAdmin):
    form = ModelScriptForm
    search_fields = (DAT_SYS_SCRIPT.TITLE,)
    list_display = (
        DAT_SYS_SCRIPT.ID,
        DAT_SYS_SCRIPT.TITLE,
        DAT_SYS_SCRIPT.DESCRIPT,
        'field_name_parent',
        'field_name_owner',
        DAT_SYS_SCRIPT.TYPE,
        DAT_SYS_SCRIPT.ENEBLED,
    )

    ordering = (
        DAT_SYS_SCRIPT.TITLE,
        DAT_SYS_SCRIPT.TYPE,
    )

    actions = [delete_scripts]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    list_editable = (
        DAT_SYS_SCRIPT.ENEBLED,
    )

    list_display_links = [
        DAT_SYS_SCRIPT.TITLE,
    ]

    readonly_fields = (DAT_SYS_SCRIPT.ID,)

    fieldsets = (
        (None,
        {'fields':
            (
                DAT_SYS_SCRIPT.ID,
                DAT_SYS_SCRIPT.TITLE,
                DAT_SYS_SCRIPT.HINT,
                (
                    DAT_SYS_SCRIPT.PARENT_ID,
                    DAT_SYS_SCRIPT.ICON,
                ),
                DAT_SYS_SCRIPT.CONTENT,
                DAT_SYS_SCRIPT.DESCRIPT,
                (
                    DAT_SYS_SCRIPT.OWNER_LINE,
                    DAT_SYS_SCRIPT.ENEBLED,
                    DAT_SYS_SCRIPT.TYPE,
                )
            )
        }),
    )
    inlines = [ModelScriptVariableAdmin]

    list_per_page = 20

    @admin.display(description='Линия')
    def field_name_owner(self, obj):
        """Линия скрипта"""
        return obj.owner

    @admin.display(description='Папка')
    def field_name_parent(self, obj):
        """Родительская папка"""
        return obj.parent


class ModelTriggerVariableAdmin(admin.TabularInline):
    model = ModelTriggerVariable


class ModelTriggerForm(forms.ModelForm):
    class Meta:
        model = ModelTrigger
        fields = '__all__'
        widgets = {
            'content': AdminMonacoEditorWidget
        }


def delete_triggers(modeladmin, request, queryset):
    for script in queryset:
        script.delete()


delete_triggers.short_description = "Удалить выбранные Триггеры"


@admin.register(ModelTrigger)
class ModelTriggerAdmin(admin.ModelAdmin):
    form = ModelTriggerForm
    list_display = (
        'get_object_title',
        DAT_SYS_TRIGGER.TITLE,
    )

    ordering = (
        DAT_SYS_TRIGGER.OBJECT_ID,
    )

    actions = [delete_triggers]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    fieldsets = (
        (None,
        {'fields':
            (
                DAT_SYS_TRIGGER.OBJECT,
                DAT_SYS_TRIGGER.TITLE,
                DAT_SYS_TRIGGER.CONTENT,
                DAT_SYS_TRIGGER.HINT,
            )
        }
        ),
    )

    inlines = [ModelTriggerVariableAdmin]

    @admin.display(description='объект')
    def get_object_title(self, obj):
        return obj.object
