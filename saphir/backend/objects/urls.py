from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list', views.aj_object_list),
    url(r'^list_type', views.aj_object_type_list),
    url(r'^list_classifier', views.aj_list_classifier),
    url(r'^object', views.aj_object),
]