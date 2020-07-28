import falcon
import json
from pymongo import MongoClient

class Resource(object):
    def on_get(self, req, resp):
        #doc = {
        #    'images': [
        #        {'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png' }
        #    ]
        #}

        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
