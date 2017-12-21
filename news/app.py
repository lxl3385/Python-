#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,abort
import os
import json

app=Flask(__name__)
#app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
db=SQLAlchemy(app)

class File(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    created_time=db.Column(db.DateTime)
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'))
    content=db.Column(db.Text)

    def __init__(self,title,created_time,content):
        self.title  =title
        self.created_time = created_time
        self.content = content

    def __repr__(self):
        return '<File %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

path="/home/shiyanlou/files/"
pages=os.listdir(path)
pagelist=[]
for page in pages:
   with open(path+page,'r') as file:
        temp=json.loads (file.read())
        pagelist.append(temp)
#print(pagelist)

def readContent(filename):
    with open(path+filename+".json") as file:
    	temp=json.loads (file.read())
    	return temp['content']

def fileisexist(filename):
    temp=os.path.exists(path+filename+".json")
    return temp
        

@app.route('/')
def index():
    return render_template('index.html',titles=pagelist)

@app.route('/files/<filename>')
def file(filename):
	if fileisexist(filename):
	    temp= readContent(filename)
	    return render_template('file.html',content=temp)
	else:
		abort(404)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404
    
