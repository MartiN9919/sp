from django.urls import path
from admin_control import views

urlpatterns = [
    path('sorted_list/', views.aj_notifications_sorted_list),
    path('', views.aj_notifications_list),
    path('<int:notification_id>/', views.aj_set_read),
]
