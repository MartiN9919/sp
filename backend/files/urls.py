from django.conf.urls import url
from files import views


urlpatterns = [
    url(r'^upload_object_file', views.aj_object_file),
]