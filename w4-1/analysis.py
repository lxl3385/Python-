#!/usr/bin/env python3
 
import pandas as pd
import sys

def analysis(file,user_id):
    data=pd.read_json(file)
    times=data[data['user_id']==user_id]['minutes'].count()
    minutes=data[data['user_id']==user_id]['minutes'].sum()
    return times,minutes

if __name__=='__main__':
    useid=int(sys.argv[1])
    data=analysis('user_study.json',useid)
    print (data)
