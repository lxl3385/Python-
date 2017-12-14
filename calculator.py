#!/home/usr/env python3

import sys
import os
from multiprocessing import Process, Queue
qCfg=Queue()
qData=Queue()
qWValue=Queue()
 
def calShui(money):
    free=money-3500     
    if free<0:
        fvalue=0
    elif free<=1500:
        fvalue=free*0.03-0
    elif free<=4500:
        fvalue=free*0.1-105
    elif free<=9000:
        fvalue=free*0.2-555
    elif free<=35000:
        fvalue=free*0.25-1005
    elif free<=55000:
        fvalue=free*0.3-2755
    elif free<=80000:
        fvalue=free*0.35-5505
    else:
        fvalue=free*0.45-13505
    return (fvalue,money-fvalue)
          
   
def CalSbao(money,ParaDic={}):
    if money<ParaDic['JiShuL']:
        BaseNum=ParaDic['JiShuL']
    elif money<ParaDic['JiShuH']:
        BaseNum=money
    else:
        BaseNum=ParaDic['JiShuH']
    Sbao=BaseNum*(ParaDic['YangLao']+ParaDic['YiLiao']+ParaDic['ShiYe']+ParaDic['GongJiJin'])
    return Sbao
       
 
def CalWvalue(Id,money,ParaDic={}):   
    Sbao=CalSbao(money,ParaDic)
    Gshui=calShui(money-Sbao)
    BasInfo=Id+','+format(money,"d" )
    Wvalue=BasInfo +','+format(Sbao,".2f" ) +','+format(Gshui[0],".2f" )+','+format(Gshui[1],".2f" )
    return Wvalue
 

#------------------------------------------
 
def readConfig(filename):   
    ParaDic={}
    with open(filename,'r') as file:
        for text in file:
            ParaList=text.split('=')
            ParaName=ParaList[0].strip()
            ParaValue=float(ParaList[1].strip())
            ParaDic[ParaName]=ParaValue
        qCfg.put(ParaDic)   
    
 
def readUser(userFile):
    IdData=[]
    with open(userFile,'r') as file:    
        for text in file:
            IdData.append(text)
        qData.put(IdData) 

def calData():
    ParaDic=qCfg.get()
    userData=qData.get() 
    Wvalue=[]
    for user in userData:
        ParaList=user.split(',')
        Wvalue.append(CalWvalue(ParaList[0],int(ParaList[1]),ParaDic)) 
    qWValue.put(Wvalue)
        

def wrtData(resultFile):
    wfree=qWValue.get()
    with open(resultFile,'w') as file:
        for free in wfree:
             print("get data"+free)
             file.write(free+'\n')
    
def main():
    Process(target=readConfig,args=(cfgFile,)).start()
    Process(target=readUser,args=(userFile,)).start()
    Process(target=calData).start()
    Process(target=wrtData,args=(resultFile,)).start()

args=sys.argv[1:]
index=args.index('-c')
cfgFile= args[index+1]
index=args.index('-d')
userFile= args[index+1]
index=args.index('-o')
resultFile= args[index+1]  

main() 
