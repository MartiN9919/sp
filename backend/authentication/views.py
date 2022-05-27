import json
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from core.projectSettings.decorators import login_check, request_wrap, request_post


@csrf_exempt
@request_wrap
@request_post
def login_user(request):
    """
    Создание сеанса пользователя
    """
    if request.user.is_authenticated:
        return {}
    body = json.loads(request.body)
    username = body['username']
    password = body['password']
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return {}
    else:
        raise Exception(400, 'Неправильный логин или пароль')


@login_check
@request_wrap
def logout_user(request):
    """
    Удаление сеанса пользователя
    """
    auth.logout(request)
    return {}


@login_check
@request_wrap
def authorization(request):
    """
    Получение данных пользователя и проверка его сеанса
    """
    return {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'admin': request.user.is_superuser,
        'staff': request.user.is_staff,
        'write': request.user.is_write,
        'group_id': {'list_id': 53, 'id': request.user.owner_groups.id}
    }



