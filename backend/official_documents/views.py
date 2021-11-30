from core.projectSettings.decorators import request_log, login_check, request_wrap
from data_base_driver.sys_reports.get_files_info import get_reports, check_progress


@login_check
@request_log
@request_wrap
def aj_reports_list(request):
    """
    Функция для обработки запроса на получение списка файлов доступных пользователю
    @param request: POST запрос на получение списка файлов доступных пользователю
    @return: список файлов в json формате
    """
    return get_reports(
        user_id=request.user.id,
        length=int(request.GET.get('size', 10)),
        offset=int(request.GET.get('offset', 0))
    )


@login_check
@request_log
@request_wrap
def aj_chek_progress(request):
    in_progress_list = [int(item) for item in request.GET.getlist('list[]')]
    return check_progress(
        request.user.id,
        in_progress_list,
        int(request.GET.get('size', 10)),
        int(request.GET.get('offset', 0))
    )
