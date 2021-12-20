from django.conf.urls import url
from objects import views


urlpatterns = [
    url(r'^get_list_obj', views.aj_object_type_list),
    url(r'^get_list_key_obj', views.aj_list_classifier),
    url(r'^get_list_key_rel', views.aj_list_rels),
    url(r'^get_lists', views.aj_lists),
    url(r'^get_tiles', views.aj_map_tiles),
    url(r'^objects_relation', views.aj_objects_relation),
    url(r'^get_object_relation', views.aj_object_relation),
    url(r'^object', views.aj_object),
    url(r'^search_relations', views.aj_search_relations),
    url(r'^search', views.aj_search_objects),
    url(r'^set_relation', views.aj_relation),
    url(r'^geometry_search', views.aj_geometry_search),
    url(r'^geometry_fc', views.aj_geometry_fc),
    url(r'^osm_search', views.aj_osm_search),
    url(r'^osm_fc', views.aj_osm_fc),
    # url(r'^groups', views.aj_groups), не используется
    # url(r'^list_icons', views.aj_list_icons), не используется
]