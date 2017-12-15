#!/home/usr/env python3
import sys   
from datetime import datetime
from multiprocessing import Process, Queue
import getopt
from configparser import ConfigParser

qData=Queue()
qWValue=Queue()

#----------------
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

#--------- 
def CalSbao(money,config): 
    if money<float(config['JiShuL']):
        BaseNum=float(config['JiShuL'])
    elif money<float(config['JiShuH']):
        BaseNum=money
    else:
        BaseNum=float(config['JiShuH'])
    Sbao=BaseNum*(float(config['YangLao'])+float(config['YiLiao'])+float(config['ShiYe'])+float(config['GongJiJin']))
    return Sbao
       
#-------------
def CalWvalue(Id,money,config):   
    Sbao=CalSbao(money,config) 
    Gshui=calShui(money-Sbao)
    BasInfo=Id+','+format(money,"d" )
    Wvalue=BasInfo +','+format(Sbao,".2f" ) +','+format(Gshui[0],".2f" )+','+format(Gshui[1],".2f" )
    return Wvalue

#------------ ----------
def readUser(userFile):
    IdData=[]
    with open(userFile,'r') as file:    
        for text in file:
            IdData.append(text)
        qData.put(IdData) 
    return IdData
  
#-------------------  
def calData(config):  
    userData=qData.get() 
    Wvalue=[]
    for user in userData: 
        ParaList=user.split(',')
        wdata=CalWvalue(ParaList[0],int(ParaList[1]),config)
        wtime=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') 
        Wvalue.append(wdata+','+wtime)  
    qWValue.put(Wvalue)
    return Wvalue
        
     
#------------------
def wrtData(resultFile):
    wfree=qWValue.get()
    with open(resultFile,'w') as file:
        for free in wfree:
            file.write(free+'\n')
   
#-----------------------------
def readComm():
    options, args = getopt.getopt(sys.argv[1:], "C:c:d:o:")
    commData={}
    for name, value in options:
        if name in ('-C'):
            commData['City']=str.upper(value)
        elif name in ('-c'):
            commData['cfgFile']=value
        elif name in ('-d'):
            commData['userFile']=value
        elif name in ('-o'):
            commData['resultFile']=value
    return commData        
    
#-----------------------

def readConf(city,filename):
    cPar=ConfigParser()   
    cPar.read(filename)
    cPar.sections()
    cfg=cPar[str.upper(city)]
    return cfg
         
#---main------------
def main():
    commData=readComm()
    print(commData)
    config=readConf('chengdu',commData['cfgFile']) 
    print(config)
    Process(target=readUser,args=(commData['userFile'],)).start()    
    Process(target=calData,args=(config,)).start() 
    Process(target=wrtData,args=(commData['resultFile'],)).start() 


if __name__ == '__main__': 
    try:
        main()
    except:
        print("Parameter Error")

