from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list_classifier', views.aj_list_classifier),
    url(r'^list_type', views.aj_object_type_list),
    url(r'^object_relation', views.aj_object_relation),
    url(r'^object', views.aj_object),
    url(r'^relations', views.aj_list_rels),
    url(r'^osm_search', views.aj_osm_search),
    url(r'^osm_fc', views.aj_osm_fc),
    url(r'^search', views.aj_search_objects),
    url(r'^relation', views.aj_relation),
    url(r'^geometry_tree', views.aj_geometry_tree),
    url(r'^geometry', views.aj_geometry),
    url(r'^groups', views.aj_groups),
    url(r'^osm_description', views.osm_geometry_hint),
    url(r'^osm_all', views.osm_geometry_all),
    url(r'^osm_geometry', views.osm_geometry),
]