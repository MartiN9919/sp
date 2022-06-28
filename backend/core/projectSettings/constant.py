import json
import os

mode = os.environ.get('MODE')

MEDIA_ROOT = '/devstorage/abiad_data' if mode != 'deploy' else '/deploy_storage/abiad_data'
DOCUMENT_ROOT = '/devstorage/abiad_documents/' if mode != 'deploy' else '/deploy_storage/abiad_documents/'
TEMPLATE_ROOT = '/devstorage/abiad_documents/template/' if mode != 'deploy' else '/deploy_storage/abiad_documents/template/'
LOG_ROOT = '/log/' if mode != 'deploy' else '/deploy_storage/abiad_log/'
MANUAL_ROOT = '/devstorage/manual/' if mode != 'deploy' else '/deploy_storage/manual/'


DEPLOY_SETTING = json.load(open('/deploy_storage/config_abiad.json')) if mode == 'deploy' else {}
