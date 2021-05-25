from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/script/', include('script.urls')),
    path('api/reports/', include('official_documents.urls')),
    path('api/objects/', include('objects.urls')),
    re_path('', TemplateView.as_view(template_name='index.html'), name='index'),
]


