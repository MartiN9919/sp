import os
from tempfile import TemporaryFile

from django.http import JsonResponse
from django.http import FileResponse
from PIL import Image

from core.projectSettings.decorators import login_check, request_log, request_get, request_download
from core.settings import MEDIA_ROOT
from data_base_driver.sys_reports.check_file_permission import check_file_permission
from data_base_driver.sys_reports.get_files_info import get_file_path
from files.additional_function import get_x_accel_response

mode = os.environ.get('MODE')


@login_check
@request_log
@request_download
def aj_download_open_file(request):
    """
    GET запрос для скачивания не защищаемого файла, характеризующего объект
    @param request: запрос на скачивание
    @return: django file response
    """
    if mode == 'deploy':
        return get_x_accel_response(request.path.split('download')[1], request.path.split('download')[1].split('/')[-1])
    else:
        file_path = MEDIA_ROOT + '/' + request.path[request.path.find('download') + 9:]
        return FileResponse(open(file_path, 'rb'), as_attachment=True)


@login_check
@request_log
@request_download
def aj_download_condense_image(request):
    """
    GET запрос для скачивания не защищаемого файла, характеризующего объект
    @param request: запрос на скачивание
    @return: django file response
    """
    file_path = MEDIA_ROOT + '/' + request.path.split('condense_image_download')[1]
    original_image = Image.open(file_path)
    width, height = original_image.size
    new_width = 250
    new_height = height/(width/new_width)
    resized_image = original_image.resize((int(new_width), int(new_height)))
    temp_file = TemporaryFile()
    resized_image.save(temp_file, "png")
    temp_file.seek(0)
    return FileResponse(temp_file)


@login_check
@request_log
@request_get
def aj_download_report(request):
    """
    Функция для загрузки пользовательского отчета
    @param request: http запрос
    @return: файл отчета
    """
    file_id = request.path.split('download_report')[1]
    if not check_file_permission(int(file_id[1:]), request.user.id):
        return JsonResponse({}, status=403)
    path = get_file_path(int(file_id[1:]))
    if os.path.exists(path):
        if mode == 'deploy':
            return get_x_accel_response('/reports' + path.split('saphir_documents')[1],
                                        path.split('saphir_documents')[1][1:])
        else:
            return FileResponse(open(path, 'rb'), as_attachment=True)
    else:
        return JsonResponse({}, status=404)