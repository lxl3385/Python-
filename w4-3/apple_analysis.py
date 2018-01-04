#!/home/usr/env python3
# -*- coding:utf-8 -*-

import pandas as pd

def quarter_volume():
    data=pd.read_csv('apple.csv',header=0)
    value=data.Volume
    value.index=pd.to_datetime(data.Date)
    mdata=value.resample('Q').sum()
    temp=mdata.sort_values()
    second_volume=temp[-2]
    print(mdata)
    return second_volume

if __name__=='__main__':
    quarter_volume()
