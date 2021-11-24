from django.urls import path
from notifications import views

urlpatterns = [
    path('', views.aj_notifications_list),
    path('<int:notification_id>/', views.aj_set_read),
]
