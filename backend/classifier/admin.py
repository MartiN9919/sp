from django.contrib import admin
from django.contrib.admin import RelatedFieldListFilter
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import models

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
    search_fields = (DAT_SYS_KEY.TITLE,)
    list_display = (DAT_SYS_LIST_TOP.TITLE, DAT_SYS_LIST_TOP.NAME)
    fieldsets = (
        (None, {'fields': ((DAT_SYS_LIST_TOP.TITLE, DAT_SYS_LIST_TOP.NAME,),)}),
    )
    ordering = (DAT_SYS_LIST_TOP.TITLE,)
    inlines = [ModelListDopAdmin]


class SpeciesFilterRelObject(RelatedFieldListFilter):
    def __init__(self, field, request, *args, **kwargs):
        """Get the species you want to limit it to.
        This could be determined by the request,
        But in this example we'll just specify an
        arbitrary species"""

        if len(args) == 3:
            self.value = args[0].get('rel_obj_1__id__exact', None)
            if not self.value:
                self.value = args[0].get('rel_obj_2__id__exact', None)
        super(SpeciesFilterRelObject, self).__init__(field, request, *args, **kwargs)

    def queryset(self, request, queryset):
        if self.value:
            return queryset.filter(Q(rel_obj_1_id=int(self.value)) | Q(rel_obj_2_id=int(self.value)))
        else:
            return queryset.filter()


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

    autocomplete_fields = (DAT_SYS_KEY.LIST,)

    fieldsets = (
        ("Название классификатора", {'fields': ((DAT_SYS_KEY.TITLE, DAT_SYS_KEY.NAME,), (DAT_SYS_KEY.PATH,),)}),
        ("Основные настройки классификатора", {'fields': (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST,), }),
        ("Описания для классификатора", {'fields': ((DAT_SYS_KEY.HINT, DAT_SYS_KEY.DESCRIPT,),), }),

        ("Поля для связи между объектами", {'fields': ((DAT_SYS_KEY.REL_OBJ_1, DAT_SYS_KEY.REL_OBJ_2,),), }),
        (None, {'fields': ((DAT_SYS_KEY.COL, DAT_SYS_KEY.NEED,),), }),
    )

    list_filter = (DAT_SYS_KEY.OBJ + '__title', (DAT_SYS_KEY.REL_OBJ_1, SpeciesFilterRelObject),
                   (DAT_SYS_KEY.REL_OBJ_2, SpeciesFilterRelObject))
    list_per_page = 20


class SpeciesFilterRel(RelatedFieldListFilter):
    def __init__(self, field, request, *args, **kwargs):
        """Get the species you want to limit it to.
        This could be determined by the request,
        But in this example we'll just specify an
        arbitrary species"""

        if len(args) == 3:
            self.value = args[0].get('rel_obj_1__id__exact', None)
            if not self.value:
                self.value = args[0].get('rel_obj_2__id__exact', None)
        super(SpeciesFilterRel, self).__init__(field, request, *args, **kwargs)

    def queryset(self, request, queryset):
        if self.value:
            return queryset.filter(Q(rel_obj_1_id=int(self.value)) | Q(rel_obj_2_id=int(self.value)), obj_id=1)
        else:
            return queryset.filter(obj_id=1)


class Rel(ModelKey):
    def save(self, *args, **kwargs):
        self.obj_id = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Классификатор связь"
        verbose_name_plural = "Классификатор связь"
        proxy = True


@admin.register(Rel)
class ModelKeyAdminRel(admin.ModelAdmin):
    list_display = (
        DAT_SYS_KEY.TITLE,
        DAT_SYS_KEY.PATH,
        DAT_SYS_KEY.TYPE_VAL,
        DAT_SYS_KEY.REL_OBJ_1,
        DAT_SYS_KEY.REL_OBJ_2,
        DAT_SYS_KEY.COL,
        DAT_SYS_KEY.NEED,

    )

    ordering = (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.PATH, DAT_SYS_KEY.TITLE,)

    autocomplete_fields = (DAT_SYS_KEY.LIST,)

    fieldsets = (
        ("Название связи", {'fields': ((DAT_SYS_KEY.TITLE, DAT_SYS_KEY.NAME,), (DAT_SYS_KEY.PATH,),)}),
        ("Основные настройки связи", {'fields': (DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST,), }),
        ("Описания для связи", {'fields': ((DAT_SYS_KEY.HINT, DAT_SYS_KEY.DESCRIPT,),), }),

        ("Поля для связи между объектами", {'fields': ((DAT_SYS_KEY.REL_OBJ_1, DAT_SYS_KEY.REL_OBJ_2,),), }),
        (None, {'fields': ((DAT_SYS_KEY.COL, DAT_SYS_KEY.NEED,),), }),
    )

    list_filter = ((DAT_SYS_KEY.REL_OBJ_1, SpeciesFilterRel),
                   (DAT_SYS_KEY.REL_OBJ_2, SpeciesFilterRel))
    list_per_page = 20


class SpeciesFilterClassifier(RelatedFieldListFilter):
    def __init__(self, field, request, *args, **kwargs):
        """Get the species you want to limit it to.
        This could be determined by the request,
        But in this example we'll just specify an
        arbitrary species"""
        if len(args) == 3:
            self.value = args[0].get('obj__id__exact', None)
        super(SpeciesFilterClassifier, self).__init__(field, request, *args, **kwargs)

    def queryset(self, request, queryset):
        if self.value:
            return queryset.filter(~Q(obj_id=1), obj_id=int(self.value))
        else:
            return queryset.filter(~Q(obj_id=1))


class ObjectKey(ModelKey):

    def clean(self):
        try:
            self.save()
        except Exception as e:
            raise e

    def save(self, *args, **kwargs):
        if self.obj_id == 1:
            raise ValidationError('в данной форме нельзя добавлять связи')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Классификатор объекта"
        verbose_name_plural = "Классификатор объекта"
        proxy = True


@admin.register(ObjectKey)
class ModelKeyAdminObject(admin.ModelAdmin):
    list_display = (
        DAT_SYS_KEY.TITLE,
        DAT_SYS_KEY.PATH,
        DAT_SYS_KEY.OBJ,
        DAT_SYS_KEY.TYPE_VAL,
        DAT_SYS_KEY.COL,
        DAT_SYS_KEY.NEED,

    )

    ordering = (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.PATH, DAT_SYS_KEY.TITLE,)

    autocomplete_fields = (DAT_SYS_KEY.LIST,)

    fieldsets = (
        ("Название классификатора", {'fields': ((DAT_SYS_KEY.TITLE, DAT_SYS_KEY.NAME,), (DAT_SYS_KEY.PATH,),)}),
        ("Основные настройки классификатора", {'fields': (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST,), }),
        ("Описания для классификатора", {'fields': ((DAT_SYS_KEY.HINT, DAT_SYS_KEY.DESCRIPT,),), }),

        (None, {'fields': ((DAT_SYS_KEY.COL, DAT_SYS_KEY.NEED,),), }),
    )

    list_filter = ((DAT_SYS_KEY.OBJ, SpeciesFilterClassifier),)
    list_per_page = 20
