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
nltk.download('maxent_ne_chunker')
nltk.download('words')

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
            cp  = RegexpParser(patterns)
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

class FindNames(object):
    @classmethod
    def on_get(self, req, resp, id):
        nnp1 = []
        nnp2 = []
        arts_obj = ArticleModel.objects().all_fields()
        for art in arts_obj:
            #print(art.to_json())
            #arts.append(art.to_json())
            titl = word_tokenize(art['title'])
            #sent = sent_tokenize(art['txt'])
            #words = [word_tokenize(xt) for xt in sent]
            #tags = [pos_tag(xt) for xt in words]
            nnp1pat = """nnp1: {<NNP.?>{1,}}"""
            nnp2pat = """nnp2: {<NNP.?>{2,}}"""
            tag = pos_tag(titl)
            cp  = RegexpParser(nnp1pat)
            rslt1 = cp.parse(tag)
            cp  = RegexpParser(nnp2pat)
            rslt2 = cp.parse(tag)
            def chkname(rslt, nnp):
                for mc in rslt:
                    if 'NNP' in mc[0]:
                        name = ""
                        for wd in mc:
                            #print(wd[0])
                            if len(wd[0]) == 1:
                                print(mc)
                                return
                            else:
                                name = name +  wd[0] + ' '
                        name = name.strip()
                        print(name)
                        #print(mc.leaves, len(mc), mc)
                        nnp.append(name)
                #if mc[:3] == "myc":
                #    print(mc)
            #chkname(rslt2, nnp2)
            chkname(rslt1, nnp1)
            #print(rslt)


            #out = nltk.chunk.ne_chunk(sent)
        #nnp2 = list(dict.fromkeys(nnp2))
        nnp1 = list(dict.fromkeys(nnp1))


        #print(nnp2)
        resp.json = { 'rslt': nnp1 }


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
anltk = NLTKArticle()
fndnam = FindNames()

api = application = falcon.API(middleware=middleware)
api.add_route('/arts/names/{id}', fndnam)
api.add_route('/arts/tst/{id}', anltk)
api.add_route('/arts/{id}', arts)
api.add_route('/images', images)

