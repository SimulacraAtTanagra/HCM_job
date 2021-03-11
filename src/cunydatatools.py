# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 10:10:55 2020

@author: shane
"""

"""
This file contains tools to read, strip, and interact with
employment data from Oracle Peoplesoft Product CUNYfirst, HCM. 
"""

from admin import newest,colclean
import pandas as pd
import json
import os
from xml.etree.ElementTree import ParseError
from xlrd import XLRDError

def rehead(df,num):
    new_header = df.iloc[(num-1)] #grab the first row for the header
    df = df[num:] #take the data less the header row
    df.columns = new_header #set the header row as the df heade
    return(df)
    
def write_json(someobj,filename):
  with open(f'{filename}.json','w') as f:
    json.dump(someobj,f)
    
    
def read_json(filename):
  if ".json" in filename:
      with open(filename,'r') as f:
          return(json.load(f))
  else:
      return(None)
      
def to_records(path,fname,reheadnum):
    df=colclean(rehead(pd.read_excel(newest(path,fname)),reheadnum))
    return(list(df.itertuples(index=False,name=None)))
    
def trydict(dicts,val):
    try:
        return(dicts[val])
    except:
        return(None)
        
def fileverify(fname):
    os.path.isfile(fname) 
    
def jsrename(emplid,download_dir):
    df=list(colclean(pd.read_html(newest(download_dir,'ps'))[0]).itertuples(index=False,name=None))
    df=[tuple([emplid]+list(i)) for i in df]
    write_json(df,f'{download_dir}//{emplid}')   
    