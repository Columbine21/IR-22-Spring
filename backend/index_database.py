from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import requests
import glob
import os
import json

import json



os.environ['CUDA_VISIBLE_DEVICES'] = ''
es = Elasticsearch()

 
type_= {
    'properties': {
        'id':{
        'type':'int'
        },

        'chinese_name': {
            'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
 
        },
        'trans_name':{
                    'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
        },
        'image_url':{
        'type':'text'
        },
            'download_url':{
        'type':'text'
        },    
        'actor':{
                       'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
            },

        'director':{
                       'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
            },
              'category':{
                       'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
            },
              
                          'date':{
                       'type': 'text',
            'analyzer': 'ik_max_word',
            'search_analyzer': 'ik_max_word'
            }
 
    }
 }


import numpy as np

def download(file_path, picture_url):
    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36           (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
                        }
    r = requests.get(picture_url,headers=headers)
    
    with open(file_path, 'wb') as f:
        f.write(r.content)
def index_database():
    alls = []
    output_hash = open("names.txt",'w',encoding='utf-8')
   # model = get_seresnet50()
    fjson = open("all_data.json",'r',encoding='utf-8')
    fin  = json.load(fjson)
    ff = json.loads(fin)
    actions = []
    for idx,item in enumerate(ff):
        if (idx%500==0):
            print(idx,"lines")

        image_file=""
        if os.path.exists("./pictures/pics/{}.jpg".format(str(idx))):
            vct = np.load("./pictures/nps/{}.npy".format(str(idx)))
            alls.append(vct)

            if (type(item["namer"])!=type("str")):
                item["namer"]="Noname"
            if (type[item["name"]]!=type("str")):
                item["name"]="Noname"
            print(idx,file=output_hash)

        if (type(item["namer"])!=type("str")):
            item["namer"]="Noname"
        if (type[item["name"]]!=type("str")):
            item["name"]="Noname"

    #images = glob.glob('static/database/*')
    

      #  cap = gencap.get_caption(image)

        image = item["image_url"]

        doc = {'id':idx,'imgurl': image, 'chinese_name':item["namer"],"trans_name":item["name"],'actor':item["main_actor"],'director':item["director"],"category":item["category"],"date":item["publish_date"],"download_url":item["download_url"]}
        for pp in doc.keys():
            if (type(doc[pp])!=str and type(doc[pp])!=int):
                doc[pp]="Null"
        actions.append(doc)
#        if (idx>0 and idx%100==0):
 #           bulk(es,actions,index="desearch1",doc_type="json")
  #          actions = []

    alls = np.array(alls)
    np.save("./output.npy",alls)
    print("saved_numpy")
    bulk(es,actions,index="desearch3",doc_type="json")
#    es.indices.put_mapping(index='news',doc_type="json",body=type_,include_type_name=True)


if __name__ == "__main__":
    index_database()
    print('Images from static/img are indexed successfully')