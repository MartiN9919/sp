from django.conf.urls import url
from notifications import views

urlpatterns = [
    url(r'^list', views.aj_notifications_list),
    url(r'^set', views.aj_set_read),
]
