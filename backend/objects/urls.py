from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list_classifier', views.aj_list_classifier),
    url(r'^list_type', views.aj_object_type_list),
    url(r'^object', views.aj_object),
    url(r'^relations', views.aj_list_rels),
    url(r'^search', views.aj_search_objects),
    url(r'^relation', views.aj_relation),
]