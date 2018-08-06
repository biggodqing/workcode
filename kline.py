
# coding: utf-8

# In[319]:


import pandas as pd
import os
import json
import time
import matplotlib.pyplot as plt
import functools


# In[210]:


data_root= "./data_root"


# In[314]:


def get_dir():
    path = '/home/data/jupyter_root/data_root/3001'
    fullpath = []
    for dirpath,dirnames,filenames in os.walk(path):
        for file in filenames:
                p=os.path.join(dirpath,file)
                fullpath.append(p)
    return fullpath

def trans_root(row_path,period=60): #transfer file path
    path_part = row_path.strip().split('/')
    if path_part[-4]=='LME': #'3001/LME/0/LMCADS03/20180725'
        date = path_part[-1]
        code = path_part[-2]
        market = path_part[-4]
        expiry_date = None
    else:
        date = path_part[-1]
        expiry_date = path_part[-2]
        code = path_part[-3]
        market = path_part[-5]
    if period == 60:
        if expiry_date == None:
            return "{meta}/{market}/{period}/{code}".format(meta=3002, market=market, period=period, code=code),date
        else:
            return "{meta_id}/{market}/{period}/{code}/{YM}".format(meta_id=3002,market=market,period=period,code=code,YM=expiry_date),date
    elif period == 86400:
        if expiry_date == None:
            return "{meta}/{market}/{period}/{code}".format(meta=3002, market=market, period=period, code=code),date
        return None

def get_key (meta_id=3002,market='SHFE',period=60,code="",YM=None,date=None): #code为jy_root_code
    if period==60:
        return "{meta_id}/{market}/{period}/{code}/{YM}/{date}".format(meta_id = meta_id,market=market,period=period,code=code,YM=YM,date=date)
    else:
        return "{meta_id}/{market}/{period}/{code}".format(meta_id = meta_id,market=market,period=period,code=code) 
    
def get_kline(x, last=[1]):
    if x.empty:
        d = {"o": last[0],"h": last[0], "l": last[0], "c":last[0], 'v':0}
    else:
        d = {"o": x.price.iloc[0],"h": x.price.max(), "l": x.price.min(), "c":x.price.iloc[-1], "v":x.vol.sum()}
        last[0] = d['c']
    return pd.Series(d)

def save(key,name,data):
    if key:
        _path = os.path.join(data_root, key)
        if not os.path.exists(_path):
            os.makedirs(_path)
        with open(os.path.join(_path, name),'w') as fp:
            data.to_json(fp, orient='records')
            
def transfer_kline(file_path,key,file_name):
    with open(file_path,'r') as fp:
        data = pd.read_json(fp)
        data.times = pd.DatetimeIndex(data.times) # .tz_localize('Asia/Shanghai')
        data = data.set_index('times')
        try:
            if len(data) == 1:
                kline_data = data.resample('T',closed='right').apply(functools.partial(get_kline,last=[data.iloc[0].price]))
#               kline_data=pd.DataFrame({"o":data_price,"h":data_price,"l":data_price,"c":data_price,'v':0},index=data.index)    
            else:
                kline_data = data.iloc[1:].resample('T',closed='right').apply(functools.partial(get_kline,last=[data.iloc[1].price]))
        except Exception as err:
            print(file_path,'error')
        kline_data['times'] = kline_data.index
        kline_data = kline_data.reindex(columns=['times','c','h','l','o','v'])
        save(key,file_name,kline_data)
        print(file_name,'finish')
        return None


# In[262]:


def transfer_all_history():
    all_file = get_dir()
    for file in all_file:
        key,file_name = trans_root(file,period=60)
        transfer_kline(file,key,file_name)
    print("all_done")
        
def transfer_daily():
    all_file = get_dir()
    file_names = set()
    for file in all_file:
        key,file_name = trans_root(file,period=60)
        file_names.add(file_name)
    file_names=sorted(list(file_names))
    date = file_names[-1]
    for file in all_file:
        key,file_name = trans_root(file,period=60)
        if file_name == date:
            transfer_kline(file,key,file_name)
        else:
            continue
    print('all done')


# In[250]:


transfer_all_history()


# In[258]:


import numpy as np
df = pd.DataFrame(np.arange(12).reshape(3,4))
len(df)


# In[315]:


data1=data.iloc[1:].resample("T", closed="right").apply(functools.partial(get_kline, last=[data.iloc[1].price])) 


# In[318]:


path = '/home/data/jupyter_root/data_root/3001/LME/0/LMCADS03/20180725'
with open(path,'r') as f:
    key,filename = trans_root(path,period=60)
    data = pd.read_json(f)
    data.times = pd.DatetimeIndex(data.times) #.tz_localize("Asia/Shanghai")# "America/New_York" "Asia/Shanghai"
    data = data.set_index('times')
    #data1=data.iloc[1:].resample("D", closed="right").apply(functools.partial(get_kline, last=[data.iloc[1].price])) 
    data1=data.resample("D", closed="right").apply(functools.partial(get_kline, last=[data.iloc[0].price])) 
    data1['times']=data1.index
    data1 = data1.reindex(columns=['times','c','h','l','o','v'])

data1


# In[208]:


with open('./data_root/3001/SHFE/0/AL/201809/20180801','r') as f:
    data = pd.read_json(f)
    data.times = pd.DatetimeIndex(data.times).tz_localize("Asia/Shanghai")# "America/New_York"
#     #data.times = pd.DatetimeIndex(([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t[:10]))) for t in ts]))
    data = data.set_index('times')
import functools
data1=data.iloc[1:].resample("D", closed="right").apply(functools.partial(get_kline, last=[data.iloc[1].price]))   # "T":minute
data1.to_json('/home/data/jupyter_root/data_root/3002/tt')


# In[329]:


path_new = '/home/data/jupyter_root/data_root/3001/SHFE/0/AL/201810'
for dirpath,dirnames,filenames in os.walk(path_new):
    l = []
    for file in filenames:
        real_path=os.path.join(dirpath,file)
        l.append(real_path)
    df_list = []
    for file in sorted(l):
        with open(file,'r') as fp:
            data = pd.read_json(fp)
            data.times = pd.DatetimeIndex(data.times)
            data = data.set_index('times')
            data1 = data.resample("D", closed="right").apply(functools.partial(get_kline, last=[data.iloc[0].price])) 
            data1['times']=data1.index
            data1 = data1.reindex(columns=['times','c','h','l','o','v'])
            df_list.append(data1)
    print(pd.concat(df_list))
            
        


# A year
# M month
# W week
# D day
# H hour
# T minute
# S second
# pandas resample params

# In[135]:


data.resample("T")

