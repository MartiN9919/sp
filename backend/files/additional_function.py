from django.http import HttpResponse


def get_x_accel_response(path, name):
    response = HttpResponse()
    path = path.encode('utf-8', 'ignore')
    name = 'attachment; filename=' + name
    name = name.encode('utf-8', 'ignore')
    response['X-Accel-Redirect'] = path
    response['Content-Disposition'] = name
    return response


def get_object_file_dir(object_id: int, rec_id: int) -> str:
    return f"/files/{object_id}/{(rec_id // 1000) + 1}/{rec_id}"


def get_object_file_path(object_id: int, rec_id: int, name: str) -> str:
    return f"{get_object_file_dir(object_id, rec_id)}/{name}"


def convert_file_path(user_path: str) -> str:
    """
    Функция для преобразования клиентского пути к файлу к серверному пути
    @param user_path: клиентский путь к файлу  /files/object_id/rec_id/name
    @return: серверный путь к файлу в формате строки /files/object_id/(object_id//1000) + 1/rec_id/name
    """
    user_path_list = user_path.split('/')
    object_id: int = int(user_path_list[2])
    rec_id: int = int(user_path_list[3])
    return get_object_file_path(object_id, rec_id, user_path.split('/')[-1])
