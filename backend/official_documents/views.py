import json
from django.http import JsonResponse, HttpResponse
from core.projectSettings.decoraters import decor_log_request, login_check
from data_base_driver.sys_reports.get_files_info import get_file_path, get_list_files_by_user
from data_base_driver.sys_reports.check_file_permission import check_file_permission


@login_check
@decor_log_request
def aj_reports_list(request):
    """
    Функция для обработки запроса на получение списка файлов доступных пользователю
    @param request: POST запрос на получение списка файлов доступных пользователю
    @return: список файлов в json формате
    """
    return JsonResponse({'data': get_list_files_by_user(request.user.id)}, status=200)


@login_check
@decor_log_request
def aj_file_download(request):
    """
    Функция для обработки запроса на скачивание файла
    @param request: POST запрос на скачивание файла
    @return: ответ для NGINX который отдает пользователю в файл,
    с учетом проверки доступа
    """
    file_id = json.loads(request.body)['id']
    if file_id == None: return JsonResponse(data={}, status=400)
    if not check_file_permission(file_id, request.user.id):
        return JsonResponse(data={}, status=403)
    path = get_file_path(file_id)
    response = HttpResponse()
    response['Content-Type'] = 'application/octet-stream'
    response["Content-Disposition"] = 'attachment; filename={}'.format(path.split('/')[-1])
    response['X-Accel-Redirect'] = '/protected/{}'.format(path)
    return response
