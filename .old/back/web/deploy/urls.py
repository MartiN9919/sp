from   django.contrib            import admin
from   django.urls               import include, path, re_path
from   django.views.generic      import RedirectView

from   map.views                 import main as map_view
from   graph.views               import main as graph_view

from   web.aj.sys                import aj_sys_error
from   web.aj.script             import aj_script_list, aj_script_exec
from   web.aj.alert              import aj_alert_set, aj_alert_get
from   web.aj.db.db_el           import aj_el_find
from   web.aj.db.db_file         import aj_panorama_get
from   web.aj.db.db_geometry     import aj_polygon_get_osm


urlpatterns = [
    path('admin/',                         admin.site.urls),
    path('auth/',                          include('authent.urls')),

    re_path(r'^map\/?$',   map_view,       name='map'),
    re_path(r'^graph\/?$', graph_view,     name='graph'),

    # AJAX
    re_path(r'^aj/script/list\/?$',        aj_script_list),                     # скрипт: список доступных скриптов
    re_path(r'^aj/script/exec\/?$',        aj_script_exec),                     # скрипт: выполнить 

    re_path(r'^aj/alert/set\/?$',          aj_alert_set),                       # оповещение: послать
    re_path(r'^aj/alert/get\/?$',          aj_alert_get),                       # оповещение: принять

    re_path(r'^aj/el/find\/?$',            aj_el_find),                         # найти элемент по поисковой фразе
    re_path(r'^aj/panorama/get\/?$',       aj_panorama_get),
    re_path(r'^aj/polygon/get/osm\/?$',    aj_polygon_get_osm),

    re_path(r'^aj/',                       aj_sys_error),                       # ошибочный ajax
    re_path(r'^',                          RedirectView.as_view(url='/map')),   # ничего не найдено - переадресация
]


