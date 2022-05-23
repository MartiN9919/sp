import json

from django.views.decorators.csrf import csrf_exempt

from vector_parser.converter import ConverterBank


@csrf_exempt
def aj_convert(request):
    if request.method == 'GET':
        try:
            path = request.GET['path']
            setting = json.load(open(path))
            converter = ConverterBank(setting)
            converter.convert()
            return True
        except Exception as e:
            raise e