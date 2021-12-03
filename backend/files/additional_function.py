from django.http import HttpResponse


def get_x_accel_response(path, name):
    response = HttpResponse()
    path = path.encode('utf-8', 'ignore')
    name = 'attachment; filename=' + name
    name = name.encode('utf-8', 'ignore')
    response['X-Accel-Redirect'] = path
    response['Content-Disposition'] = name
    return response