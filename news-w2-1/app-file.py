#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,abort
from datetime import datetime
from sqlalchemy import create_engine
import os
import json

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root@localhost/shiyanlou'
db=SQLAlchemy(app)
engine=create_engine('mysql://root@localhost/shiyanlou')
#-----------------------------
class File(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    created_time=db.Column(db.DateTime)
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'))
    category=db.relationship('Category',backref=db.backref('posts',lazy='dynamic'))
    content=db.Column(db.Text)

    def __init__(self,title,created_time,category,content):
        self.title  =title
        self.created_time = created_time
        self.category=category 
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

#--------------------------------
def readDir(path):
    pages=os.listdir(path)
    pagelist=[]
    for page in pages:
        with open(path+page,'r') as file:
            temp=json.loads (file.read())
            pagelist.append(temp)
    return pagelist
#print(pagelist)

def readFile(filename):    
    with open(path+filename+".json") as file:
    	temp=json.loads (file.read())
    	return temp

def fileisexist(filename):
    temp=os.path.exists(path+filename+".json")
    return temp
        
path="/home/shiyanlou/files/"
#----------------
    

@app.route('/')
def index():
    pagelist=readDir(path)
    return render_template('index.html',titles=pagelist)

@app.route('/files/<filename>')
def file(filename):
	if fileisexist(filename):
	    temp= readFile(filename)
	    return render_template('file.html',file=temp)
	else:
		abort(404)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404
    
