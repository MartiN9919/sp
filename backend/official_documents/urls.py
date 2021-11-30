from django.conf.urls import url
from official_documents import views

urlpatterns = [
    url(r'^list', views.aj_reports_list),
    url(r'^check_progress', views.aj_check_progress)
]
