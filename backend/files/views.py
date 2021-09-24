import os

from django.http import JsonResponse
from django.http import FileResponse
from PIL import Image

from core.projectSettings.decoraters import login_check, request_log, request_get
from core.settings import MEDIA_ROOT
from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.sys_reports.check_file_permission import check_file_permission
from data_base_driver.sys_reports.get_files_info import get_file_path


@login_check
@request_log
@request_get
def aj_download_open_file(request):
    """
    GET запрос для скачивания не защищаемого файла, характеризующего объект
    @param request: запрос на скачивание
    @return: django file response
    """
    path = request.path.split('download_open_files')[1]
    path_start_directory = path.split('/')[1]
    if path_start_directory != 'open_files':
        return JsonResponse({}, status=403)
    object_id = int(path.split('/')[2])
    rec_id = int(path.split('/')[3])

    # временно пока не развернут nginx
    file_path = MEDIA_ROOT + '/' + path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        return JsonResponse({}, status=404)


@login_check
@request_log
@request_get
def aj_download_condense_image(request):
    """
    GET запрос для скачивания не защищаемого файла, характеризующего объект
    @param request: запрос на скачивание
    @return: django file response
    """
    path = request.path.split('download_condense_image')[1]
    path_start_directory = path.split('/')[1]
    if path_start_directory != 'open_files':
        return JsonResponse({}, status=403)
    # временно пока не развернут nginx
    file_path = MEDIA_ROOT + '/' + path
    if os.path.exists(file_path):
        original_image = Image.open(file_path)
        width, height = original_image.size
        new_width = 250
        new_height = height/(width/new_width)
        resized_image = original_image.resize((int(new_width), int(new_height)))
        new_file_path = 'temp.' + file_path.split('/')[-1].split('.')[-1]
        resized_image.save(new_file_path)
        temp_file = open(new_file_path, 'rb')
        os.remove(new_file_path)
        return FileResponse(temp_file)
    else:
        return JsonResponse({}, status=404)


@login_check
@request_log
@request_get
def aj_download_report(request):
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    file_id = request.path.split('download_report')[1]
    if not check_file_permission(int(file_id[1:]), group_id):
        return JsonResponse({}, status=403)
    path = get_file_path(int(file_id[1:]))
    if os.path.exists(path):
        return FileResponse(open(path, 'rb'), as_attachment=True)
    else:
        return JsonResponse({}, status=404)