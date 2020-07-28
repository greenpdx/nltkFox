import falcon
import json
from .images import Resource
import os
import falcon_jsonify
import mongoengine as mongo
from mongoengine import *
import datetime
import pymongo
from bson.objectid import ObjectId

import nltk
#from nltk.corpus import brown
#from pattern.en import parse, parsetree
from nltk.tokenize import word_tokenize

from nltk import pos_tag
from nltk import sent_tokenize
from nltk import RegexpParser

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

dbcfg = {
    'host': '10.0.42.168', # or external server address
    'port': 27017,
    #'username': os.environ.get('MONGO_USER'),
    'username': 'ubuntu',
    #'password': os.environ.get('MONGO_PASS'),
    'password': 'ubuntu',
}
middleware = [
    falcon_jsonify.Middleware(help_messages=True),
]

class ArticleModel(Document):
    #_id = ObjectIdField(required=True)
    meta = {
        'collection': 'prelp'
    }
    _id = ObjectIdField()
    title = StringField(max_length=100, required=True)
    href = URLField(max_length=100, required=True, unique=True)
    ts = FloatField(required=True)
    pri = IntField()
    kr = StringField(max_length=100)
    h1 = StringField(max_length=100, required=True)
    h2 = StringField(max_length=100)
    txt = StringField(max_length=10000, required=True)
    last = FloatField()

class NLTKArticle(object):
    @classmethod
    def on_get(self, req, resp, id):
        print(id)
        if (len(id) > 0):
            arts_obj = ArticleModel.objects(_id=ObjectId(id) )
            art = arts_obj[0]
            print(art['href'])
            title = art['title']
            toks = word_tokenize(title)
            sent = sent_tokenize(art['txt'])
            sent = [word_tokenize(xt) for xt in sent]
            sent = [pos_tag(xt) for xt in sent]
            print(sent)
            tag = pos_tag(toks)
            grammar = "NP: {<DT>?<JJ>*<NN>}"
            patterns= """mychunk:{<NN.?>*<VBD.?>*<JJ.?>*<CC>?}"""
            cp  = RegexpParser(grammar)
            rslt = cp.parse(tag)
            print(rslt)
            resp.json = { 'rslt': str(rslt) }
        else:
            #resp.status = falcon.HTTP_200
            #arts = []
            #arts_obj = ArticleModel.objects().all_fields()
            #for art in arts_obj:
                #print(art.to_json())
            #    arts.append(art.to_json())
            callnames = ['tst']
            resp.json = { 'rslt': json.dumps(callnames)}



class GetArticles(object):
    @classmethod
    def on_get(self, req, resp, id):
        print(id)
        if (len(id) > 0):
            arts_obj = ArticleModel.objects(_id=ObjectId(id) )
            art = arts_obj[0]

            resp.json = { 'rslt': art.to_json() }
        else:
            resp.status = falcon.HTTP_200
            arts = []
            arts_obj = ArticleModel.objects().all_fields()
            for art in arts_obj:
                #print(art.to_json())
                arts.append(art.to_json())
            resp.json = { 'rslt': arts}

db = mongo.connect('foxnews2',
    host=dbcfg['host'],
    port=dbcfg['port'],
    #username=dbcfg['username'],
    #password=dbcfg['password']
)
print(db)
images = Resource()
arts = GetArticles()
nltk = NLTKArticle()

api = application = falcon.API(middleware=middleware)
api.add_route('/arts/tst/{id}', nltk)
api.add_route('/arts/{id}', arts)
api.add_route('/images', images)

