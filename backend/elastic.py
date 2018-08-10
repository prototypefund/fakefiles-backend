"""
bridge `backend.Item` between elasticsearch backend from `image_match`
"""

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

from django.conf import settings


es = Elasticsearch(hosts=[settings.ES_HOST])
ses = SignatureES(es, index=settings.ES_INDEX)


def add_image(path, metadata={}):
    ses.add_image(path, metadata=metadata)


def setup_elasticsearch(reset=False):
    index = settings.ES_INDEX
    if not es.indices.exists(index):
        es.indices.create(index)
        deleted = False
        created = True
    else:
        if reset:
            es.indices.delete(index)
            es.indices.create(index)
            deleted = True
            created = True
        else:
            created = False
            deleted = False
    return deleted, created
