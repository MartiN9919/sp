from django.conf.urls import url
from script import views


urlpatterns = [
    url(r'^get_list_script', views.aj_script_list),
    url(r'^get_list_trigger', views.aj_trigger_list),
    url(r'^get_list_template', views.aj_templates_list),
    url(r'^get_template', views.aj_template),
    url(r'^exec_map', views.aj_script_execute_map),
    url(r'^exec_report', views.aj_script_execute_report),
]