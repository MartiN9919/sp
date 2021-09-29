from django.conf.urls import url
from files import views


urlpatterns = [
    url(r'^download_condense_image', views.aj_download_condense_image),
    url(r'^download_open_file', views.aj_download_open_file),
    url(r'^download_report', views.aj_download_report),
]