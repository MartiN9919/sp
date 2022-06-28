from django.contrib import admin
from django.contrib.admin import RelatedFieldListFilter
from django.db.models import Q

from classifier.models import ModelObject, ModelList, ModelListDop, ModelPhoneNumberFormat, ObjectKey, Rel
from data_base_driver.constants.const_admin import PROJECT_TITLE_ADMIN
from data_base_driver.constants.const_dat import DAT_SYS_KEY, DAT_SYS_OBJ, DAT_SYS_LIST_TOP, \
    DAT_SYS_PHONE_NUMBER_FORMAT, DAT_SYS_LIST_DOP

admin.site.site_header = PROJECT_TITLE_ADMIN


@admin.register(ModelObject)
class ModelObjectAdmin(admin.ModelAdmin):

    list_display = (
        DAT_SYS_OBJ.ID,
        DAT_SYS_OBJ.TITLE,
        DAT_SYS_OBJ.NAME,
        DAT_SYS_OBJ.PRIORITY
    )
    list_display_links = (DAT_SYS_OBJ.TITLE,)
    readonly_fields = (DAT_SYS_OBJ.ID, DAT_SYS_OBJ.NAME)
    fieldsets = (
        ('Идентификатор', {'fields': ((DAT_SYS_OBJ.ID, DAT_SYS_OBJ.NAME),)}),
        ("Имя Объекта", {'fields': ((DAT_SYS_OBJ.TITLE, DAT_SYS_OBJ.TITLE_SINGLE),)}),
        ('Описание объекта', {'fields': ((DAT_SYS_OBJ.PRIORITY, DAT_SYS_OBJ.ICON),)}),
        ('Информация для администраторов', {
            'classes': ('collapse',),
            'fields': (DAT_SYS_OBJ.DESCRIPT,)
        })
    )
    ordering = [DAT_SYS_OBJ.PRIORITY]

    def has_delete_permission(self, request, obj=None):
        """
        Отключение возможности удаления объектов
        """
        return False


@admin.register(ModelListDop)
class ModelListAdmin(admin.ModelAdmin):
    search_fields = [DAT_SYS_LIST_DOP.VAL]
    ordering = [DAT_SYS_LIST_DOP.ID]
    list_per_page = 20

    def get_model_perms(self, request):
        """
        Костыль для скрытия сквозных значений списков
        """
        return {}


class ModelListDopAdmin(admin.TabularInline):
    search_fields = [DAT_SYS_LIST_DOP.VAL]
    autocomplete_fields = (DAT_SYS_LIST_DOP.PARENT,)
    readonly_fields = (DAT_SYS_LIST_DOP.ID, )
    fieldsets = (
        (None, {'fields': ((DAT_SYS_LIST_DOP.ID, DAT_SYS_LIST_DOP.VAL, DAT_SYS_LIST_DOP.PARENT),)}),
    )
    model = ModelListDop


@admin.register(ModelList)
class ModelListAdmin(admin.ModelAdmin):
    list_display = (DAT_SYS_LIST_TOP.ID, DAT_SYS_LIST_TOP.TITLE, DAT_SYS_LIST_TOP.NAME)
    list_display_links = (DAT_SYS_LIST_TOP.TITLE,)
    search_fields = (DAT_SYS_LIST_TOP.TITLE,)
    readonly_fields = (DAT_SYS_LIST_TOP.ID, DAT_SYS_LIST_TOP.NAME)
    fieldsets = (
        ("Идентификатор", {
            'fields': ((DAT_SYS_LIST_TOP.ID, DAT_SYS_LIST_TOP.NAME),)
        }),
        (None, {'fields': (DAT_SYS_LIST_TOP.TITLE,)}),
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
            self.object_id_1 = args[0].get('rel_obj_1__id__exact', None)
            self.object_id_2 = args[0].get('rel_obj_2__id__exact', None)
            self.value = args[0].get('rel_obj_1__id__exact', None)
            if not self.value:
                self.value = args[0].get('rel_obj_2__id__exact', None)
        super(SpeciesFilterRel, self).__init__(field, request, *args, **kwargs)

    def queryset(self, request, queryset):
        if self.object_id_1 and self.object_id_2:
            return queryset.filter((Q(rel_obj_1_id=int(self.object_id_1)) & Q(rel_obj_2_id=int(self.object_id_2))) |
                                   (Q(rel_obj_1_id=int(self.object_id_2)) & Q(rel_obj_2_id=int(self.object_id_1))),
                                   obj_id=1)
        elif self.value:
            return queryset.filter(Q(rel_obj_1_id=int(self.value)) | Q(rel_obj_2_id=int(self.value)), obj_id=1)
        else:
            return queryset.filter(obj_id=1)


@admin.register(Rel)
class ModelKeyAdminRel(admin.ModelAdmin):
    list_display = (
        DAT_SYS_KEY.ID,
        DAT_SYS_KEY.TITLE,
        DAT_SYS_KEY.REL_OBJ_1,
        DAT_SYS_KEY.REL_OBJ_2,
        DAT_SYS_KEY.COL,
        DAT_SYS_KEY.NEED,
        DAT_SYS_KEY.DESCRIPT,
    )
    list_display_links = (DAT_SYS_KEY.TITLE,)
    search_fields = [DAT_SYS_KEY.TITLE, ]
    ordering = (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.TITLE,)

    autocomplete_fields = (DAT_SYS_KEY.LIST,)
    readonly_fields = (DAT_SYS_KEY.ID, DAT_SYS_KEY.NAME)
    fieldsets = (
        ("Идентификатор", {
            'fields': ((DAT_SYS_KEY.ID, DAT_SYS_KEY.NAME),)
        }),
        ("Основные настройки", {
            'fields': (
                DAT_SYS_KEY.TITLE, (DAT_SYS_KEY.REL_OBJ_1, DAT_SYS_KEY.REL_OBJ_2), DAT_SYS_KEY.LIST, DAT_SYS_KEY.NEED,
            ),
        }),
        ("Отображение", {
            'fields': (DAT_SYS_KEY.PRIORITY, DAT_SYS_KEY.BLOCKED_IN_BLANK),
        }),
        ('Информация для пользователей', {
            'classes': ('collapse',),
            'fields': (DAT_SYS_KEY.HINT,)
        }),
        ('Информация для администраторов', {
            'classes': ('collapse',),
            'fields': (DAT_SYS_KEY.DESCRIPT,)
        })
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


@admin.register(ObjectKey)
class ModelKeyAdminObject(admin.ModelAdmin):
    list_display = (
        DAT_SYS_KEY.ID,
        DAT_SYS_KEY.TITLE,
        DAT_SYS_KEY.OBJ,
        DAT_SYS_KEY.PRIORITY,
        DAT_SYS_KEY.TYPE_VAL,
        DAT_SYS_KEY.LIST,
        DAT_SYS_KEY.NEED,
        DAT_SYS_KEY.DESCRIPT,
    )
    list_display_links = (DAT_SYS_KEY.TITLE,)
    search_fields = [DAT_SYS_KEY.TITLE, ]

    ordering = (DAT_SYS_KEY.OBJ, DAT_SYS_KEY.PRIORITY, DAT_SYS_KEY.TITLE,)

    autocomplete_fields = (DAT_SYS_KEY.LIST,)
    readonly_fields = (DAT_SYS_KEY.ID,DAT_SYS_KEY.NAME)
    fieldsets = (
        ("Идентификатор", {
            'fields': ((DAT_SYS_KEY.ID, DAT_SYS_KEY.NAME),)
        }),
        ("Основные настройки", {
            'fields': (
                DAT_SYS_KEY.TITLE, DAT_SYS_KEY.OBJ, DAT_SYS_KEY.NEED,
            ),
        }),
        ("Тип", {
            'fields': (DAT_SYS_KEY.TYPE_VAL, DAT_SYS_KEY.LIST,)
        }),
        ("Отображение", {
            'fields': (DAT_SYS_KEY.PRIORITY, DAT_SYS_KEY.VISIBLE, DAT_SYS_KEY.BLOCKED_IN_BLANK),
        }),
        ('Информация для пользователей', {
            'classes': ('collapse',),
            'fields': (DAT_SYS_KEY.HINT,)
        }),
        ('Информация для администраторов', {
            'classes': ('collapse',),
            'fields': (DAT_SYS_KEY.DESCRIPT,)
        })
    )

    list_filter = ((DAT_SYS_KEY.OBJ, SpeciesFilterClassifier),)
    list_per_page = 20

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            temp = request.GET.get('_changelist_filters', '')
            if temp.find('obj__id__exact') != -1:
                obj_id = temp.split('obj__id__exact')[1].split('=')[1].split('&')[0]
            else:
                obj_id = '0'
            form.base_fields['obj'].initial = int(obj_id)
        return form
