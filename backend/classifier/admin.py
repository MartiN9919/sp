from django.contrib import admin
from django.contrib.admin import RelatedFieldListFilter
from django.core.exceptions import ValidationError
from django.db.models import Q
from classifier.models import ModelKey, ModelObject, ModelList, ModelListDop, ModelPhoneNumberFormat
from data_base_driver.constants.const_admin import PROJECT_TITLE_ADMIN
from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_SYS_OBJ, DAT_SYS_LIST_TOP, DAT_SYS_PHONE_NUMBER_FORMAT

admin.site.site_header = PROJECT_TITLE_ADMIN


@admin.register(ModelObject)
class ModelObjectAdmin(admin.ModelAdmin):
    list_display = (
        DAT_SYS_OBJ.ID,
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


@admin.register(ModelPhoneNumberFormat)
class ModelPhoneNumberFormatAdmin(admin.ModelAdmin):
    search_fields = (DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY,)
    list_display = (DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY, DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY_CODE,
                    DAT_SYS_PHONE_NUMBER_FORMAT.LENGTH,)
    fieldsets = (
        (None, {'fields': ((DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY, DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY_CODE,
                    DAT_SYS_PHONE_NUMBER_FORMAT.LENGTH,),)}),
    )
    ordering = (DAT_SYS_PHONE_NUMBER_FORMAT.COUNTRY,)


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
        DAT_SYS_KEY.ID,
        DAT_SYS_KEY.REL_OBJ_1,
        DAT_SYS_KEY.REL_OBJ_2,
        DAT_SYS_KEY.COL,
        DAT_SYS_KEY.NEED,
        DAT_SYS_KEY.DESCRIPT,
    )
    search_fields = [DAT_SYS_KEY.TITLE, ]
    ordering = (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.TITLE,)

    autocomplete_fields = (DAT_SYS_KEY.LIST,)
    readonly_fields = (DAT_SYS_KEY.ID,)
    fieldsets = (
        ("Идентификатор", {'fields': (DAT_SYS_KEY.ID,)}),
        ("Название связи", {'fields': ((DAT_SYS_KEY.TITLE, DAT_SYS_KEY.NAME,), )}),
        ("Основные настройки связи", {'fields': (DAT_SYS_KEY.LIST,), }),
        ("Описания для связи", {'fields': ((DAT_SYS_KEY.HINT,),), }),
        ("Поля для связи между объектами", {'fields': ((DAT_SYS_KEY.REL_OBJ_1, DAT_SYS_KEY.REL_OBJ_2,),), }),
        (None, {'fields': ((DAT_SYS_KEY.BLOCKED_IN_BLANK),), }),
        ("Дополнительная информация", {'fields': (DAT_SYS_KEY.DESCRIPT,), }),
    )

    list_filter = ((DAT_SYS_KEY.REL_OBJ_1, SpeciesFilterRel),
                   (DAT_SYS_KEY.REL_OBJ_2, SpeciesFilterRel))
    list_per_page = 20

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            filter_str = request.GET.get('_changelist_filters', '0=0&0=0').split('&')
            if len(filter_str) == 1:
                obj_id_1 = int(filter_str[0].split('=')[1])
                form.base_fields['rel_obj_1'].initial = int(obj_id_1)
                return form
            else:
                obj_id_1 = int(filter_str[0].split('=')[1])
                obj_id_2 = int(filter_str[1].split('=')[1])
                form.base_fields['rel_obj_1'].initial = int(obj_id_1)
                form.base_fields['rel_obj_2'].initial = int(obj_id_2)
                return form
        else:
            return form


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
        DAT_SYS_KEY.ID,
        DAT_SYS_KEY.OBJ,
        DAT_SYS_KEY.PRIORITY,
        DAT_SYS_KEY.TYPE_VAL,
        DAT_SYS_KEY.NEED,
        DAT_SYS_KEY.DESCRIPT,
    )
    search_fields = [DAT_SYS_KEY.TITLE, ]

    ordering = (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.PRIORITY, DAT_SYS_KEY.TITLE,)

    autocomplete_fields = (DAT_SYS_KEY.LIST,)
    readonly_fields = (DAT_SYS_KEY.ID,)
    fieldsets = (
        ("Идентификатор", {'fields': (DAT_SYS_KEY.ID,)}),
        ("Название классификатора", {'fields': ((DAT_SYS_KEY.TITLE, DAT_SYS_KEY.NAME,), (DAT_SYS_KEY.PRIORITY, ),)}),
        ("Основные настройки классификатора", {'fields': (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST, ), }),
        ("Описания для классификатора", {'fields': ((DAT_SYS_KEY.HINT,),), }),
        (None, {'fields': ((DAT_SYS_KEY.NEED, DAT_SYS_KEY.VISIBLE, DAT_SYS_KEY.BLOCKED_IN_BLANK),), }),
        ("Дополнительная информация", {'fields': (DAT_SYS_KEY.DESCRIPT,), }),
    )

    list_filter = ((DAT_SYS_KEY.OBJ, SpeciesFilterClassifier),)
    list_per_page = 20

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            obj_id = request.GET.get('_changelist_filters', '0=0').split('=')[1]
            form.base_fields['obj'].initial = int(obj_id)
        return form
