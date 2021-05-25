from django.contrib         import admin
from admin_dop.models       import ModelAlerts, ModelScript, ModelOwnerLine

from lib.const              import PROJECT_TITLE_ADMIN
from lib.db.const.const_dat import DAT_SYS_ALERT, DAT_SYS_SCRIPT


admin.site.site_header = PROJECT_TITLE_ADMIN



##################################################################################
# DAT_SYS_ALERT
##################################################################################
@admin.register(ModelAlerts)
class ModelAdminAlerts(admin.ModelAdmin):
    """
    Регистрация таблицы sys_alert на странице администратора
    """

    list_display = (
        DAT_SYS_ALERT.ID,
        DAT_SYS_ALERT.CONTENT,
        DAT_SYS_ALERT.DESCRIPT,
        DAT_SYS_ALERT.TYPE,
        DAT_SYS_ALERT.WAIT,
        DAT_SYS_ALERT.GROUPS,
        DAT_SYS_ALERT.ENABLED,
    )

    # сортировка
    ordering = (
        DAT_SYS_ALERT.ID,
        # '-'+DAT_SYS_ALERT.ENABLED,
    )

    # список редактируемых полей - первое поле list_display не ставить
    list_editable = (
        DAT_SYS_ALERT.CONTENT,
        DAT_SYS_ALERT.DESCRIPT,
        DAT_SYS_ALERT.TYPE,
        DAT_SYS_ALERT.WAIT,
        DAT_SYS_ALERT.GROUPS,
        DAT_SYS_ALERT.ENABLED,
    )

    # # фильтр
    # list_filter = (
    #     DAT_SYS_ALERT.TYPE,
    #     DAT_SYS_ALERT.ENABLED,
    # )

    # # поиск по полям
    # search_fields = (
    #     DAT_SYS_ALERT.CONTENT,
    # )

    #readonly_fields  = (DAT_SYS_ALERT.ID,)
    list_per_page     = 15                                                                              # записей на страницу
    actions_on_top    = False                                                                           # расположение поля управления записями
    actions_on_bottom = False                                                                           # расположение поля управления записями
    actions           = None                                                                            # отключить все действия
    # owner_line = models.ForeignKey(
    #     ModelOwnerLine,
    #     on_delete=models.CASCADE,
    #     verbose_name='Группа владельцев',
    # )
    # РЕДАКТОР ЗАПИСИ
    fieldsets = (
        (None,
        {'fields':
            (
                (
                    DAT_SYS_ALERT.CONTENT,
                    DAT_SYS_ALERT.DESCRIPT,
                ),
                (
                    DAT_SYS_ALERT.USERS,
                    DAT_SYS_ALERT.GROUPS,
                ),
                DAT_SYS_ALERT.OWNER,
                DAT_SYS_ALERT.TYPE,
                DAT_SYS_ALERT.WAIT,
                DAT_SYS_ALERT.ENABLED,
            )
        }),
    )
    save_on_top      = False
    save_as          = True                                                                             # кнопка "Сохранить как новый объект"
    save_as_continue = False

    class Media:
        js  = ('/static/admin_base.js',)
        css = {'all': ('/static/admin_base.css',)}


@admin.register(ModelScript)
class ModelScriptAdmin(admin.ModelAdmin):
    list_display = (
        'get_parent',
        'get_name',
        DAT_SYS_SCRIPT.DESCRIPT,
        'get_owner',
        DAT_SYS_SCRIPT.ENEBLED,
    )

    ordering = (
        DAT_SYS_SCRIPT.NAME,
    )

    list_editable = (
        DAT_SYS_SCRIPT.ENEBLED,
    )

    list_display_links = [
        'get_name',
    ]

    fieldsets = (
        (None,
         {'fields':
             (
                 DAT_SYS_SCRIPT.NAME,
                 DAT_SYS_SCRIPT.HINT,
                 (
                     DAT_SYS_SCRIPT.PARENT,
                     DAT_SYS_SCRIPT.ICON,
                 ),
                 DAT_SYS_SCRIPT.CONTENT,
                 DAT_SYS_SCRIPT.DESCRIPT,
                 DAT_SYS_SCRIPT.VARIABLES,
                 (
                     DAT_SYS_SCRIPT.OWNER,
                     DAT_SYS_SCRIPT.ENEBLED,
                 )
             )
         }),
    )

    list_per_page = 15
    actions_on_top = False
    actions_on_bottom = False
    actions = None
    save_on_top = False
    save_as = True                                                                             # кнопка "Сохранить как новый объект"
    save_as_continue = False

    class Media:
        js = ('/static/admin_base.js',)
        css = {'all': ('/static/admin_base.css',)}

    def get_owner(self, obj):
        """
        Функция, взвращающая тип пользователя
        """
        return obj.owner

    def get_parent(self, obj):
        """
        Функция, взвращающая родительскую папку
        """
        return obj.parent

    def get_name(self, obj):
        """
        Функция, взвращающая имя объекта, параллельно определяя, чем этот объект является
        """
        if obj.icon:
            return 'Папка ' + obj.name
        else:
            return obj.name
