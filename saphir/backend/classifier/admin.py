from django.contrib import admin
from .models import ModelKey, ModelObject, ModelList, ModelListDop

from data_base_driver.constants.const_admin import PROJECT_TITLE_ADMIN
from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_SYS_OBJ, DAT_SYS_LIST_TOP

admin.site.site_header = PROJECT_TITLE_ADMIN


@admin.register(ModelObject)
class ModelObjectAdmin(admin.ModelAdmin):
    list_display = (
        DAT_SYS_OBJ.TITLE,
        DAT_SYS_OBJ.TITLE_SINGLE,
        DAT_SYS_OBJ.NAME,
        DAT_SYS_OBJ.DESCRIPT
    )
    fieldsets = (
        ("Имя Объекта", {'fields': ((DAT_SYS_OBJ.TITLE, DAT_SYS_OBJ.TITLE_SINGLE,),)}),
        ('Транслитерация объекта', {'fields': (DAT_SYS_OBJ.NAME,)}),
        ('Пометки', {'fields': (DAT_SYS_OBJ.DESCRIPT,)}),
    )
    ordering = [DAT_SYS_OBJ.TITLE]


class ModelListDopAdmin(admin.TabularInline):
    model = ModelListDop


@admin.register(ModelList)
class ModelListAdmin(admin.ModelAdmin):
    list_display = (DAT_SYS_LIST_TOP.TITLE, DAT_SYS_LIST_TOP.NAME)
    fieldsets = (
        (None, {'fields': ((DAT_SYS_LIST_TOP.TITLE, DAT_SYS_LIST_TOP.NAME,),)}),
    )
    inlines = [ModelListDopAdmin]


@admin.register(ModelKey)
class ModelKeyAdmin(admin.ModelAdmin):
    list_display = (
        DAT_SYS_KEY.TITLE,
        DAT_SYS_KEY.OBJ,
        DAT_SYS_KEY.TYPE_VAL,
        DAT_SYS_KEY.REL_OBJ_1,
        DAT_SYS_KEY.REL_OBJ_2,
        DAT_SYS_KEY.COL,
        DAT_SYS_KEY.NEED,
    )

    fieldsets = (
        ("Название классификатора", {'fields': ((DAT_SYS_KEY.TITLE, DAT_SYS_KEY.NAME,),)}),
        ("Основные настройки классификатора", {'fields': (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST,), }),
        ("Описания для классификатора", {'fields': ((DAT_SYS_KEY.HINT, DAT_SYS_KEY.DESCRIPT,),), }),
        ("Поля для связи между объектами", {'fields': ((DAT_SYS_KEY.REL_OBJ_1, DAT_SYS_KEY.REL_OBJ_2,),), }),
        (None, {'fields': ((DAT_SYS_KEY.COL, DAT_SYS_KEY.NEED,),), }),
    )

    list_filter = (DAT_SYS_KEY.OBJ + '__title', DAT_SYS_KEY.REL_OBJ_1, DAT_SYS_KEY.REL_OBJ_2)
    list_per_page = 20
