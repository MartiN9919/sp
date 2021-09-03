import json
import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse

from core.projectSettings.decoraters import login_check, request_log, request_get
from core.settings import MEDIA_ROOT
from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.input_output.input_output import io_set

@login_check
@request_log
@request_get
def aj_download(request):
    path = request.path.split('download')[1]
    path_start_directory = path.split('/')[1]
    if path_start_directory != 'open_files':
        return JsonResponse({}, status=403)
    # временно пока не развернут nginx
    file_path = MEDIA_ROOT + '/' + path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="files")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        return JsonResponse({}, status=404)
