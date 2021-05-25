from django.conf.urls import url

from dat import views

urlpatterns = [
    url(r'^', views.main),
    #url(r'^', views.all),
]
