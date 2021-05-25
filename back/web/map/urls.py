from django.conf.urls import url
from django.urls import path

from .views import main as map_view
from web.aj.script import aj_script_list, aj_script_exec

urlpatterns = [
    path('', map_view, name='map'),  # возвращает html страницы map
    path('list/', aj_script_list),  # скрипт: список доступных скриптов для страницы map
    path('exec/', aj_script_exec),  # скрипт: выполнить скрипт по его id с параметрами
]
