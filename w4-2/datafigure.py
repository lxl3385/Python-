#!/usr/bin/env python3
  
import pandas as pd 
import matplotlib.pyplot as plt

#if __name__=='__main__': 

fig=plt.figure()
#ax=fig.add_subplot(1,1,1)

data=pd.read_json('user_study.json') 
x=data['user_id']
xx=x.drop_duplicates()
y=data[['user_id','minutes']].groupby('user_id').sum()

py=y.plot()
py.set_title("StudyData")
py.set_xlabel("User ID")
py.set_ylabel("Study Time")

fig.show()
