import glob
import os
import numpy as np
from PIL import Image
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from flask import Flask, render_template, request, Response, jsonify
from werkzeug.utils import secure_filename
import json
from torch.autograd import Variable
import torch
import torch.nn as nn
from torchvision import datasets, models
import torchvision.transforms as transforms
img_to_tensor = transforms.ToTensor()
resnet18_model = models.resnet18(pretrained=True)
resnet18_model.to("cpu")
TARGET_IMG_SIZE=224
es = Elasticsearch()
import faiss
index = faiss.IndexFlatL2(1000)
vcts = np.load("./output.npy")
index.add(vcts)
fin = open("./names.txt",'r',encoding='utf-8')
names_ = fin.readlines()
names = []
for item in names_:
    line = item.strip()
    names.append(int(line))


def extract_feature(model, imgpath):
    img = Image.open(imgpath).convert('RGB')  # 读取图片
    img = img.resize((TARGET_IMG_SIZE, TARGET_IMG_SIZE))

    tensor = img_to_tensor(img)  # 将图片矩阵转化成tensor
    tensor = tensor.cpu()  # GPU
    tensor = torch.unsqueeze(tensor, 0)
    result = model(Variable(tensor))
    result_npy = result.data.cpu().numpy()
    assert len(result_npy.shape)==2 and result_npy.shape[0]==1
    return result_npy

from flask_cors import CORS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'database')
app.config['TEMP_UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png'])
CORS(app,supports_credentials=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']




@app.route('/keywordSearch', methods=['GET', 'POST'])
def caption():
    #not available
    has_pic = False

    self_dct = request.json
    if has_pic:
        matches = []
        for item in ids:
            body = {
            "size":1,
             "query":{
                "match":{"id":item}
            }
            }
            matches.append(es.search(index="desearch",body=body)["hits"]["hits"][0]["_source"])

        final_output=matches
        data = {"data":final_output,"totalCount":len(final_output)}
        return json.dumps(data, ensure_ascii=False)
    else:
        lsts = []
        page = 0
        print(self_dct.keys())
        if True:
            try:
                page = 20*int(self_dct["pageNo"])
            except:
                page = 0
            print(self_dct.keys())
            if (len(self_dct.keys())<=1):
                print("only_page")
                body = {
                "query":{
                "match_all":{}
              },
              "from":0,  # 从第二条数据开始
              "size":1000  # 获取4条数据
                }

                output = es.search(index="desearch", body=body)
                hits = output["hits"]["hits"]
            #    print(len(hits),"total_len")
                final_output = []
                for _hit in hits:
                    hit = _hit["_source"]
                    new_format = {}
                    for k in hit.keys():
                        new_format[k]=hit[k]
                    final_output.append(new_format)
                if len(final_output)>page+20:
                    pages = final_output[page:page+20]
                else:
                    pages = final_output[:20]
                data = {"data":pages,"totalCount":len(final_output)}
                return json.dumps(data, ensure_ascii=False)







            for k,v in self_dct.items():
                if (k!="pageNo"):
                    lsts.append({"match":{k:v}})
            bl = {"must":lsts}
            body = {
             "query":{
                "bool":bl
            },
              "sort": [
                { "_score": { "order": "desc" }}
            ],
            "from":0,
            "size":1000

            }
            output = es.search(index="desearch", body=body)



            hits = output["hits"]["hits"]
            final_output = []
            for _hit in hits:
                hit = _hit["_source"]
                new_format = {}
                for k in hit.keys():
                    new_format[k]=hit[k]
                final_output.append(new_format)
           # print(final_output)
            
            if len(final_output)>page+20:
                pages = final_output[page:page+20]
            else:
                pages = final_output[:20]
            data = {"data":pages,"totalCount":len(final_output)}
            resp = json.dumps(data, ensure_ascii=False)
  #  resp.headers['Access-Control-Allow-Origin'] = request.headers.get(
  #      'Origin') or 'http://127.0.0.1:1024'
  #  resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
 #   resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return resp




@app.route('/upload', methods=['GET', 'POST'])
def up():
    #not available
    has_pic = False
  #  print(request,"q")
  #  print(request.form.to_dict()["key"],"qq")
  #  print(request.json)
  #  print(request.files)
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '' or not allowed_file(
                request.files['file'].filename):
            has_pic=False
        else:   
            file = request.files['file']
            img = Image.open(file.stream)  # PIL image
            uploaded_img_path = os.path.join("tmp", file.filename)
            img.save(uploaded_img_path)
            feat = extract_feature(resnet18_model,uploaded_img_path)
         #   print(feat)
          #  print(vcts[0])
         #   feat = np.array([vcts[0]])
            print(index.ntotal)
            D,I = index.search(feat,10)
            ids = [names[ite] for ite in I[0]] 
            print(I)
            print(ids)
            has_pic = True

    self_dct = request.json
    if has_pic:
        matches = []
        for item in ids:
            body = {
            "size":1,
             "query":{
                "match":{"id":item}
            }
            }
            matches.append(es.search(index="desearch",body=body)["hits"]["hits"][0]["_source"])

        final_output=matches
        data = {"data":final_output,"totalCount":len(final_output)}
        print(data)
        return json.dumps(data, ensure_ascii=False)





if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=8090)
