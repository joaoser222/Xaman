from django.shortcuts import render
from django.db.models import Q
import app.models as models
import glob,os,json,pandas as pd,numpy as np
from sqlalchemy import create_engine,inspect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .snippets import *

class Register(APIView):
  permission_classes = ()
  authentication_classes = ()
  def post(self,request):
    data = request.data
    password = data.pop('password',None)
    confirm_password = data.pop('confirm_password',None)
    try:
      user = models.User(**data)
      user.set_password(password)
      user.full_clean()
      if(password!=confirm_password):
        return Response({'errors':{'confirm_password':['As senhas não coincidem!']}},422)    
      user.save()
    except ValidationError as e:
      return Response({'errors':e.message_dict},422)
    except Exception as e:
      return Response({'errors':e},500)
    return Response({'success':'Cadastro efetuado com sucesso!'})

class Query(APIView):
  permission_classes = ()
  authentication_classes = ()
  def post(self,request):
    dataset = request.data['dataset']
    string_connection = dataset['engine']+'://'+dataset['username']+':'+dataset['password']+'@'+dataset['host']+'/'+dataset['database']
    engine = create_engine(string_connection)
    query = engine.connect().execute(request.data['code'])
    data = []
    columns = query.keys()
    for row in query:
      obj = {column: '' for column in columns}
      for idx,item in enumerate(row):
        if str(type(item))=="<class 'NoneType'>":
          obj[columns[idx]] = 'null'
        else:
          obj[columns[idx]] = '%s' % item
      data.append(obj)
    return Response({'data': data,'columns': columns})

class Dataset(APIView):
  permission_classes = ()
  authentication_classes = ()
  def get(self,request):
    if request.args.get('dataset') is None:
      datasets = serializer(models.Dataset.objects.all())
      return Response(datasets)
    else:
      dataset = serializer(models.Dataset.objects.filter(name=request.args.get('dataset')))
      engine = create_engine(dataset['engine']+'://'+dataset['username']+':'+dataset['password']+'@'+dataset['host']+'/'+dataset['database'])
      data = {'dataset':dataset,'objects':[]}
      for table in engine.table_names():
        children = {'label':table,'icon':'icon-browsers-outline','children':[]}
        columns = inspect(engine).get_columns(table,schema=dataset['database'])
        for column in columns:
          children['children'].append({'label':column['name'],'icon':'icon-reader-outline'})
        data['objects'].append(children)
      return Response(data)

  def post(self,request):
    data = request.data
    if 'id' in data:
      dataset = models.Dataset.objects.get(data['id'])
      for item in data:
        setattr(dataset, item, data[item])
        dataset.save()
      return Response({'success': 'Registro atualizado com successo!'})
    else:
      models.Dataset(**data).save()
      return Response({'success': 'Cadastro efetuado com sucesso!'})

  def delete(self,request):
    models.Dataset.objects.get(data['id']).delete()
    return Response({'success': 'Registro deletado com sucesso!'})

class FileManager(APIView):
  permission_classes = ()
  authentication_classes = ()
  def get(self,request):
    data = response.data
    path =  os.path.expanduser('~') if not('path' in data.keys()) else data['path']
    extensions =  data['extensions'] if len(data['extensions'].split(','))<=1 else tuple(data['extensions'].lower().split(','))
    if os.path.isfile(path):
      file = open(path,'r')
      return Response({'content':file.read(),'path':path,'name':path.split('/')[-1]})
    else:
      folders = []
      files = []
      for item in glob.glob("%s/*" % path):
        obj = {}
        if os.path.isdir(item):
          obj['name'] = item.split('/')[-1]
          obj['type'] = 'folder'
          folders.append(obj)            
        elif item.lower().endswith(extensions):
          obj['name'] = item.split('/')[-1]
          obj['type'] = 'file'
          files.append(obj)
      return Response({'path':path,'items':folders+files})