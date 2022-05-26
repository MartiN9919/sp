import os

mode = os.environ.get('MODE')

MEDIA_ROOT = '/devstorage/saphir_data' if mode != 'deploy' else '/deploy_storage/saphir_data'
DOCUMENT_ROOT = '/devstorage/saphir_documents/' if mode != 'deploy' else '/deploy_storage/saphir_documents/'
TEMPLATE_ROOT = '/devstorage/saphir_documents/template/' if mode != 'deploy' else '/deploy_storage/saphir_documents/template/'
