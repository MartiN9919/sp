from django.contrib import admin
from django.contrib.admin import RelatedFieldListFilter

from .models import ModelKey, ModelObject, ModelList, ModelListDop, ModelKeyGroup

from data_base_driver.constants.const_admin import PROJECT_TITLE_ADMIN
from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_SYS_OBJ, DAT_SYS_LIST_TOP, DAT_SYS_KEY_GROUP

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


class SpeciesFilter(RelatedFieldListFilter):
    def __init__(self, field, request, *args, **kwargs):
        """Get the species you want to limit it to.
        This could be determined by the request,
        But in this example we'll just specify an
        arbitrary species"""
        # id1 = ''
        # if len(args) == 3:
        #     id1 = args[0]['rel_obj_1__id__exact']
        #     args2 = (args[0], {'rel_obj_2__id__exact':id1},args[1],args[2])
        #     super(SpeciesFilter, self).__init__(field, request, *args2, **kwargs)
        super(SpeciesFilter, self).__init__(field, request, *args, **kwargs)




@admin.register(ModelKey)
class ModelKeyAdmin(admin.ModelAdmin):
    list_display = (
        DAT_SYS_KEY.TITLE,
        DAT_SYS_KEY.PATH,
        DAT_SYS_KEY.OBJ,
        DAT_SYS_KEY.TYPE_VAL,
        DAT_SYS_KEY.REL_OBJ_1,
        DAT_SYS_KEY.REL_OBJ_2,
        DAT_SYS_KEY.COL,
        DAT_SYS_KEY.NEED,

    )

    ordering = (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.PATH, DAT_SYS_KEY.TITLE,)

    fieldsets = (
        ("Название классификатора", {'fields': ((DAT_SYS_KEY.TITLE, DAT_SYS_KEY.NAME, ), (DAT_SYS_KEY.PATH, ), )}),
        ("Основные настройки классификатора", {'fields': (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST,), }),
        ("Описания для классификатора", {'fields': ((DAT_SYS_KEY.HINT, DAT_SYS_KEY.DESCRIPT,),), }),
        ("Поля для связи между объектами", {'fields': ((DAT_SYS_KEY.REL_OBJ_1, DAT_SYS_KEY.REL_OBJ_2,),), }),
        (None, {'fields': ((DAT_SYS_KEY.COL, DAT_SYS_KEY.NEED,),), }),
    )

    list_filter = (DAT_SYS_KEY.OBJ + '__title', (DAT_SYS_KEY.REL_OBJ_1, SpeciesFilter), DAT_SYS_KEY.REL_OBJ_2)
    list_per_page = 20





@admin.register(ModelKeyGroup)
class ModelKeyGroupAdmin(admin.ModelAdmin):
    list_display = (
        DAT_SYS_KEY_GROUP.NAME,
        DAT_SYS_KEY_GROUP.OBJ,
        DAT_SYS_KEY_GROUP.POS,
    )
