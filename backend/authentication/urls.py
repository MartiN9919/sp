from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^authentication/login/', views.login_user),
    url(r'^authentication/logout/', views.logout_user),
    url(r'^authorization/', views.authorization),
    url(r'^is_staff', views.is_staff),
]