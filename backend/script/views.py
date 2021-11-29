import datetime
import importlib
import json
import threading

from authentication.models import ModelCustomUser
from core.settings import DOCUMENT_ROOT
from data_base_driver.script.get_script_info import get_script_title
from data_base_driver.script.script_execute import execute_script_map
from data_base_driver.script.script_list import get_script_tree
from data_base_driver.constants.const_dat import DAT_OWNER
from core.projectSettings.decorators import request_log, login_check, request_wrap, script_wrap
from data_base_driver.sys_reports.set_file_info import add_file
from data_base_driver.sys_templates.get_template_info import get_templates_list, get_template
from data_base_driver.sys_templates.set_templates_info import add_template, remove_template, update_template
from data_base_driver.trigger.trigger_list import get_triggers_list


@login_check
@request_log
@request_wrap
def aj_script_list(request):
    """
    Функция для обработки запроса на получение списка скриптов
    @param request: GET запрос на получение списка скриптов
    @return: список скриптов с учетом уровня доступа пользователя, в формате JSON
    """
    script_type = request.GET['script_type']
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    return get_script_tree(group_id, script_type)


@login_check
@request_log
@request_wrap
def aj_trigger_list(request):
    """
    Функция для обработки запроса на получение списка триггеров
    @param request: GET запрос на получение списка триггеров
    @return: список триггеров в формате JSON
    """
    return get_triggers_list()


@login_check
@request_log
@request_wrap
@script_wrap
def aj_script_execute_map(request):
    """
    Функция обработки запроса на исполнение скрипта анализа для карты
    @param request: POST запроса на исполнение скрипта анализа
    @return: json с результатом выполнения скрипта и статусом выполнения
    или текстом и кодом ошибки
    """
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    data = json.loads(request.body)
    method_name = 'script_' + str(data.get('id'))
    importlib.invalidate_caches()
    result = execute_script_map(method_name, group_id, data.get('variables'))
    return result


@login_check
@request_log
@request_wrap
@script_wrap
def aj_script_execute_report(request):
    """
    Функция для обработки запросов анализа с получением отчета
    @param request: полученный http запрос
    @return: http ответ с информацией о файле который будет подготовлен, либо информация об ошибке
    """
    data = json.loads(request.body)
    method_name = 'script_' + str(data.get('id'))
    user = ModelCustomUser.objects.get(id=request.user.id)
    title = get_script_title(data.get('id')) + '-' + datetime.datetime.now().replace(microsecond=0,
                                                                                     tzinfo=None).isoformat(sep='-')
    group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
    try:
        my_module = importlib.import_module('script.user_scripts.' + method_name)
        date_time = datetime.datetime.now()
        file_id = add_file(path=DOCUMENT_ROOT + title,
                           user_id=request.user.id,
                           params=json.dumps(data, ensure_ascii=False),
                           date_auto_remove=date_time,
                           )
        script_function = getattr(my_module, method_name)
        lock = threading.Lock()
        with lock:
            thread = threading.Thread(target=script_function,
                                      args=(data.get('variables'), group_id, file_id, request.user.id, title, lock))
            thread.start()
            return {'id': file_id, 'name': title,
                    'date': date_time.replace(microsecond=0, tzinfo=None).isoformat(sep=' '),
                    'status': 'in_progress', 'params': data}
    except Exception as e:
        raise e


@login_check
@request_log
@request_wrap
def aj_templates_list(request):
    """
    Функция для обработки запроса на получение списка шаблонов
    @param request: POST запрос на получение списка шаблонов
    @return: список шаблонов в формате json
    """
    return get_templates_list(request.user.id)


@login_check
@request_log
@request_wrap
def aj_template(request):
    """
    Функция для обработки запросов CRUD для шаблона
    @param request: GET, POST, PUT или DELETE запрос на изменение шаблона
    @return: статус выполнения либо код ошибки
    """

    if request.method == 'GET':
        try:
            return get_template(request.GET['template_id'], request.user.id)
        except:
            raise Exception(497, '')
    elif request.method == 'POST':
        group_id = DAT_OWNER.DUMP.get_group(user_id=request.user.id)
        data = json.loads(request.body)
        id = add_template(group_id, data.get('title', 'Неизвестное имя'), data.get('activeAnalysts', ''),
                          data.get('passiveAnalysts', ''))
        return id

    elif request.method == 'PUT':
        data = json.loads(request.body)
        try:
            update_template(data.get('id'), request.user.id, data.get('title'), data.get('activeAnalysts', ''),
                            data.get('passiveAnalysts', ''))
            return {}
        except Exception as e:
            raise e
    elif request.method == 'DELETE':
        try:
            remove_template(request.user.id, request.GET['template_id'])
            return {}
        except Exception as e:
            raise e
    else:
        raise Exception(470, '')

