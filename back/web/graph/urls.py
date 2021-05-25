from django.urls import path

from .views import main as graph_view

urlpatterns = [
    path(r'', graph_view),
]
