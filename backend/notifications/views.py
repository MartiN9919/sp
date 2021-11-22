import json

from core.projectSettings.decorators import login_check, request_log, request_wrap
from data_base_driver.sys_notifications.get_notifications_info import get_notifications_by_user
from data_base_driver.sys_notifications.set_notifications_info import set_read


@login_check
@request_log
@request_wrap
def aj_notifications_list(request):
    """
    Функция для обработки запроса на получение списка триггеров
    @param request: GET запрос на получение списка триггеров
    @return: список триггеров в формате JSON
    """
    notifications_list = [int(item) for item in request.GET.getlist('list[]')]
    return get_notifications_by_user(request.user.id, notifications_list)


@login_check
@request_log
@request_wrap
def aj_set_read(request):
    user_id = request.user.id
    notification_id = int(request.GET['id'])
    return set_read(notification_id, user_id)