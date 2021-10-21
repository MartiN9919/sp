from django.conf.urls import url
from files import views


urlpatterns = [
    url(r'^download_report', views.aj_download_report),
    url(r'^condense_image_download', views.aj_download_condense_image),
    url(r'^download', views.aj_download_open_file),
]