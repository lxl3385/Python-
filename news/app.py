#!/usr/bin/env python3
from flask import Flask
from flask import render_template,abort
import os
import json

app=Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True

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
    
