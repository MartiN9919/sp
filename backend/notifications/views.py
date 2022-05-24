from core.projectSettings.decorators import login_check, request_wrap
from data_base_driver.sys_notifications.get_notifications_info import get_notifications_by_user, \
    get_notifications_list_by_offset
from data_base_driver.sys_notifications.set_notifications_info import set_read


@login_check
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
@request_wrap
def aj_set_read(request, notification_id):
    """
    Функция для обработки запроса на установку флага прочитанного уведомления
    @param request: запрос
    @param notification_id: идентификатор оповещения
    @return: -
    """
    return set_read(notification_id, request.user.id)


@login_check
@request_wrap
def aj_notifications_sorted_list(request):
    """
    Функция для обработки Get запроса на получение ранжированного списока оповещений
    @param request: Get запрос
    @return: json содержащий список оповещений по заданным параметрам и общее их количество
    """
    return get_notifications_list_by_offset(request.user.id,
                                            int(request.GET.get('size', 10)),
                                            int(request.GET.get('offset', 0)),
                                            request.GET.get('date'),
                                            request.GET.get('type'),
                                            request.GET.get('order')
                                            )
