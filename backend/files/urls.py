from django.conf.urls import url
from django.urls import path

from files import views


urlpatterns = [
    url(r'^download_report', views.aj_download_report),
    url(r'^condense_image_download', views.aj_download_condense_image),
    url(r'^download', views.aj_download_open_file),
    url(r'^manuals', views.aj_get_manuals),
    path('manual/<int:manual_id>', views.aj_get_manual)
]
