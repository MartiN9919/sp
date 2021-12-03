import os

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from core import settings

mode = os.environ.get('MODE')
INDEX_PATH = 'index_dev.html'
if mode == 'deploy' or mode == 'test_deploy':
    INDEX_PATH = 'index.html'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/auth/', include('authentication.urls')),
                  path('api/script/', include('script.urls')),
                  path('api/reports/', include('official_documents.urls')),
                  path('api/objects/', include('objects.urls')),
                  path('api/files/', include('files.urls')),
                  path('api/notifications/', include('notifications.urls')),
                  re_path(r'^(?!.*admin)', TemplateView.as_view(template_name=INDEX_PATH), name='index'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
