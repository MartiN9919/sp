from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^list', views.aj_reports_list),
    url(r'^get', views.aj_file_download),
]
