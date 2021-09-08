import os

from django.http import JsonResponse
from django.http import FileResponse
from PIL import Image

from core.projectSettings.decoraters import login_check, request_log, request_get
from core.settings import MEDIA_ROOT


@login_check
@request_log
@request_get
def aj_download(request):
    """
    GET запрос для скачивания не защищаемого файла, характеризующего объект
    @param request: запрос на скачивание
    @return: django file response
    """
    path = request.path.split('download')[1]
    path_start_directory = path.split('/')[1]
    if path_start_directory != 'open_files':
        return JsonResponse({}, status=403)
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
