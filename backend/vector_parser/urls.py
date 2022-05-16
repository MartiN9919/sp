from django.conf.urls import url
from vector_parser import views

urlpatterns = [
    url(r'^convert', views.aj_convert),
]