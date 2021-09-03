import json
import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse

from data_base_driver.constants.const_dat import DAT_OWNER
from data_base_driver.input_output.input_output import io_set


def aj_object_file(request):
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    data = request.POST
    object_id = data.get('object_id')
    rec_id = data.get('rec_id')
    key_id = int(data.get('key_id'))
    path = 'open_files/' + str(object_id) + '/' + str(rec_id) + '/'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    files = request.FILES
    result = {'ok': [], 'error': []}
    for file_name in files:
        file = files[file_name]
        temp_path = default_storage.save(path + file.name, ContentFile(file.read()))
        temp_rec_id = io_set(group_id, object_id, [key_id, temp_path])
        if temp_rec_id != rec_id:
            result['error'].append(file.name)
        else:
            result['ok'].append(file.name)
    return JsonResponse({'data': result}, status=200)
