import json
import os

mode = os.environ.get('MODE')

MEDIA_ROOT = '/devstorage/saphir_data' if mode != 'deploy' else '/deploy_storage/saphir_data'
DOCUMENT_ROOT = '/devstorage/saphir_documents/' if mode != 'deploy' else '/deploy_storage/saphir_documents/'
TEMPLATE_ROOT = '/devstorage/saphir_documents/template/' if mode != 'deploy' else '/deploy_storage/saphir_documents/template/'
LOG_ROOT = '/log/' if mode != 'deploy' else '/deploy_storage/log/'
MANUAL_ROOT = 'manual/'


DEPLOY_SETTING = json.load(open('/deploy_storage/config.json')) if mode == 'deploy' else {}
