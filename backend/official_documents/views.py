from core.projectSettings.decorators import request_log, login_check, request_wrap
from data_base_driver.sys_reports.get_files_info import get_list_files_by_user


@login_check
@request_log
@request_wrap
def aj_reports_list(request):
    """
    Функция для обработки запроса на получение списка файлов доступных пользователю
    @param request: POST запрос на получение списка файлов доступных пользователю
    @return: список файлов в json формате
    """
    return get_list_files_by_user(
        user_id=request.user.id,
        length=int(request.GET.get('size', 10)),
        offset=int(request.GET.get('offset', 0))
    )
