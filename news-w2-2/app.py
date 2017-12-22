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

#--------------

def GetAll(table):
    comm='select * from '+table
    datas=engine.execute(comm).fetchall()
    idlist=[]
    for data in datas:
        temp={}
        temp['id']=data[0]
        temp['title']=data[1]
        idlist.append(temp)
    return idlist

def GetInfo(table,id):
    comm='select * from ' +table+' where id= '+id
    datas=engine.execute(comm).fetchall()
    info=[]
    for data in datas:
        temp={}
        temp['id']=data[0]
        temp['title']=data[1]
        temp['create_time']=data[2]
        temp['content']=data[4]
        info.append(temp)
    return info[0]

#----------
GetInfo('file','1')

@app.route('/')
def index():
    pagelist=GetAll('file')
    return render_template('index.html',titles=pagelist)

@app.route('/files/<file_id>')
def file(file_id):
    data = GetInfo('file',file_id)
    if len(data)!=0:
        return render_template('file.html',file=data)
    else:
        abort(404)

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404
    
