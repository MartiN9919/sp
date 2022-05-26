import json
import logging

from core.projectSettings.logging_settings import PROJECT_LOG_REQUESTS

logger = logging.getLogger(PROJECT_LOG_REQUESTS)


def logging_middleware(get_response):
    def middleware(request):
        try:
            body_string = str(request.body.decode("utf-8"))
            if len(body_string) != 0 and json.loads(request.body).get('password'):
                body = json.loads(request.body)
                body['password'] = '***'
                body_string = str(body)

            logger.info(
                str(request.user) + '.' +
                str(request.user.id) + '|' +
                request.META.get('REMOTE_ADDR') + ':' +
                str(request.META.get('REMOTE_PORT')) + '|' +
                request.method + ':' +
                request.path + '|' +
                body_string
            )
        except:
            logger.info(
                str(request.user) + '.' +
                str(request.user.id) + '|' +
                request.META.get('REMOTE_ADDR') + ':' +
                str(request.META.get('REMOTE_PORT')) + '|' +
                request.method + ':' +
                request.path + '|' +
                request.POST.get('data', '')
            )
        return get_response(request)

    return middleware

