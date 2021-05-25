from django.conf.urls import url

from authent import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^', views.all),
]
