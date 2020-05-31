from app import app
from flask import render_template,request, redirect,url_for 
import glob,os,json,pandas as pd,numpy as np
from sqlalchemy import create_engine,inspect
from flask_login import current_user, login_user,logout_user
from app.models import db, Dataset, User, AlchemyEncoder

@app.before_request
def hook():
    if(('api/auth' in request.path) & (not current_user.is_authenticated)):
       return redirect('/')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/auth/teste')
def teste():
    return json.dumps({'teste':'d'})

@app.route('/api/login', methods=['POST'])
def login():
    if request.json['email']:
        user = User.query.filter_by(email=request.json['email']).first()
        if user is None or not user.check_password(request.json['password']):
            return json.dumps({'error':'Email ou senha inválidos!'})
        login_user(user)
        return json.dumps({'success': 'Login efetuado com sucesso!'})
    else:
        return json.dumps({'error':'Email ou senha invállidos!'})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    password = data['password']
    del data['password'], data['confirm_password']
    user = User(**data)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return json.dumps({'success': 'Cadastro efetuado com sucesso!'})

@app.route('/api/check-login')
def check_login():
    if current_user.is_authenticated:
        return json.dumps({'success': User.query.get(current_user.get_id()).token})
    return json.dumps({'error': 'O usuário não está logado!'}),401

@app.route('/api/logout',methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/api/auth/query', methods=['POST'])
def query():
    dataset = request.json['dataset']
    string_connection = dataset['engine']+'://'+dataset['username']+':'+dataset['password']+'@'+dataset['host']+'/'+dataset['database']
    engine = create_engine(string_connection)
    query = engine.connect().execute(request.json['code'])
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
    return json.dumps({'data': data,'columns': columns})

@app.route('/api/auth/datasets', methods=['GET','POST','DELETE'])
def datasets():
    if request.method == 'GET':
        if request.args.get('dataset') is None:
            datasets = Dataset.query.all()
            return json.dumps(datasets, cls=AlchemyEncoder)
        else:
            dataset = json.loads(json.dumps(Dataset.query.filter_by(name=request.args.get('dataset')).first(),cls=AlchemyEncoder))
            engine = create_engine(dataset['engine']+'://'+dataset['username']+':'+dataset['password']+'@'+dataset['host']+'/'+dataset['database'])
            data = {'dataset':dataset,'objects':[]}
            for table in engine.table_names():
                children = {'label':table,'icon':'las la-table','children':[]}
                columns = inspect(engine).get_columns(table,schema=dataset['database'])
                for column in columns:
                    children['children'].append({'label':column['name'],'icon':'las la-columns'})
                data['objects'].append(children)
            return json.dumps(data)

    elif request.method == 'POST':
        request.json['user_id'] = current_user.get_id()
        if 'id' in request.json:
            dataset = Dataset.query.get(request.json['id'])
            for item in request.json:
                setattr(dataset, item, request.json[item])
            db.session.commit()
            return json.dumps({'success': 'Registro atualizado com successo!'})
        else:
            dataset = Dataset(**request.json)
            db.session.add(dataset)
            db.session.commit()
        
            return json.dumps({'success': 'Cadastro efetuado com sucesso!'})

    elif request.method == 'DELETE':
        dataset = Dataset.query.get(request.json['id'])
        db.session.delete(dataset)
        db.session.commit()
        return json.dumps({'success': 'Registro deletado com sucesso!'})

@app.route('/api/auth/files', methods=['POST','GET'])
def files():
    path =  os.path.expanduser('~') if request.json.get('path') is None else request.json['path']
    extensions =  request.json.get('extensions') if len(request.json.get('extensions').split(','))<=1 else tuple(request.json['extensions'].lower().split(','))
    
    
    if os.path.isfile(path):
        file = open(path,'r')
        return json.dumps({'content':file.read(),'path':path,'name':path.split('/')[-1]})
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
        return json.dumps({'path':path,'items':folders+files})