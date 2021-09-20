from django.conf.urls import url
from files import views


urlpatterns = [
    url(r'^download_condense_image', views.aj_download_condense_image),
    url(r'^download', views.aj_download),
]