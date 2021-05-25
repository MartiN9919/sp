from django.contrib         import admin
from admin_dop.models       import Model_Alerts

from lib.const              import PROJECT_TITLE_ADMIN
from lib.db.const.const_dat import DAT_SYS_ALERT

# Регистрируем модели в админке
#admin.site.register(Model_Alerts)

# заголовок
admin.site.site_header = PROJECT_TITLE_ADMIN
#admin.site.site_title  = PROJECT_TITLE_ADMIN


##################################################################################
# DAT_SYS_ALERT
##################################################################################
@admin.register(Model_Alerts)
class ModelAdmin_Alerts(admin.ModelAdmin):
    # СПИСОК ЗАПИСЕЙ

    # отображаемые поля в виде таблицы
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
