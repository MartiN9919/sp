from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list', views.aj_script_list),
    url(r'^execute_map', views.aj_script_execute_map),
    url(r'^execute_report', views.aj_script_execute_report),
    url(r'^templates', views.aj_templates_list),
    url(r'^template', views.aj_template),
]