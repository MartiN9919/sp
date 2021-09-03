from django.conf.urls import url
from files import views


urlpatterns = [
    url(r'^download', views.aj_download),
]