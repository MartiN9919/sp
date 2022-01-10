from django.db import models

from django_monaco_editor.fields import MonacoEditorField


class MonacoEditorModelField(models.TextField):
    def formfield(self, **kwargs):
        new_kwargs = {
            'form_class': MonacoEditorField,
        }
        new_kwargs.update(kwargs)
        return super(MonacoEditorModelField, self).formfield(**new_kwargs)
