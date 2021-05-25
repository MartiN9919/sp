import json
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.projectSettings.decoraters import decor_log_request, login_check


@csrf_exempt
@decor_log_request
def login_user(request):
    """
    Создание сеанса пользователя
    """
    # если пользователь уже залогинен, чего не может быть, но всеже возвращаем положительный результат аутентификации
    if request.user.is_authenticated:
        return JsonResponse({'status': 'Пользователь уже авторизирован'}, status=200)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # обработка входа в систему
    if request.method == 'POST':
        username = body['username']
        password = body['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return JsonResponse({'user': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }}, status=200)
        else:
            return JsonResponse({'status': 'Проверьте введенные данные'}, status=400)
    else:
        return JsonResponse({'status': 'its not POST request'}, status=403)


@login_check
@decor_log_request
def logout_user(request):
    """
    Удаление сеанса пользователя
    """
    auth.logout(request)
    return JsonResponse({}, status=200)



@login_check
@decor_log_request
def authorization(request):
    """
    Получение данных пользователя и проверка его сеанса
    """
    return JsonResponse({'user': {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }}, status=200)
