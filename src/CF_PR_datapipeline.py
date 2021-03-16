# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 20:00:33 2021

@author: shane
"""

import pandas as pd
import numpy as np
from admin import colclean, newest,rehead,read_json
from datetime import datetime

#TODO map the PR-Assist departments to HCM departments
#TODO add automated retrieval to cover the front end of this pipeline
#TODO 

def pr_data(filefolder,flag=None):
    #getting the data that appears on the PAF
    #TODO when automatically retrieving this data, please also change the name
    cols=['date', 'ctrl', 'last_nasme', 'first_nm', 'emplid', 'hcm_dept',
       'program_name', 'action', 'original', 'title', 'begin_date', 'end_date',
       'payserv_position_#:', 'budget_line_#:', 'ledger', 'fis_dept',
       'expense', 'payserv_empl_id:', 'budget_source1', 'budget_source_2',
       'budget_source3', 'hours_1', 'hours_2', 'hours_3', 'subtotal',
       'subtotal.1', 'subtotal.2', 'hourscombo', 'rate', 'total_cost',
       'student_status', 'report_to', 'sep_date']
    pafs=pd.read_excel(newest(filefolder,"paf_data"),header=None)
    pafs=pafs[[3,5,9,10,11,14,15,18,19,23,24,25,32,33,34,35,36,37,39,41,
                   43,45,47,49,51,53,55,58,59,61,63,65,68]]
    pafs.columns=cols
    #and some of the background data we also need to feed CF
    tl=colclean(pd.read_excel(newest(filefolder,"tl_data")))
    #merging
    collist=['date','hcm_dept','program_name', 'action', 'title',
           'payserv_position', 'budget_line','report_to', 'name', 'emplid', 'title',
           'dept', 'paf_type', 'rate', 'hours','end_date']
    together=pd.concat([pafs,tl],axis=1)
    together.columns=['date', 'ctrl', 'last_nasme', 'first_nm', 'emplid', 'hcm_dept',
       'program_name', 'action', 'original', 'title1', 'begin_date1', 'end_date1',
       'payserv_position', 'budget_line', 'ledger', 'fis_dept',
       'expense', 'payserv_empl_id:', 'budget_source1', 'budget_source_2',
       'budget_source3', 'hours_1', 'hours_2', 'hours_3', 'subtotal',
       'subtotal.1', 'subtotal.2', 'hourscombo', 'rate1', 'total_cost',
       'student_status', 'unnamed:_31', 'report_to', 'name', 'ss', 'title',
       'dept', 'deptarment_name', 'paf_type', 'rate', 'status', 'bgt_hrs',
       'worked', 'bgn_date', 'end_date']
    #and now let's chop the columns we don't need
    hours=[x.split()[-2] for x in together.hourscombo.replace(np.nan, '0 0 0').values]
    together['hours']=hours
    together=together[collist]
    pdict=read_json(newest(filefolder,"programcode"))
    tl=tl[tl.dept.isna()==False]
    tl['dept']=tl.dept.apply(lambda x: pdict[x])
    tl['dept']=tl.dept.apply(lambda x: pdict[x])
    together.columns=['date','hcm_dept','program_name', 'action', 'title',
           'payserv_position', 'budget_line','report_to', 'name', 'empl_id', 'title',
           'dept_id_job', 'paf_type', 'rate', 'bgt_hrs','end_date']
    
    together['combo']=together['empl_id'].astype('str')+together['dept_id_job'].astype('str')
    #and grabbing CF data to get record
    df=colclean(rehead(pd.read_excel(newest(filefolder,"FULL_FILE"),engine='xlrd'),2))
    #removing unnecessary columns
    ndf=df[['empl_id', 'empl_rcd','effdt_job', 'effseq_job','jobcode_cd','dept_id_job','action_ld','action_reason_ld']]
    ndf.empl_id=ndf.empl_id.astype('O')
    deletions=ndf[ndf.jobcode_cd=='500050'][ndf.action_reason_ld.str.contains("Mass System Termination")]
    ndf=ndf[ndf.jobcode_cd=='500050'][~ndf.action_reason_ld.str.contains("Mass System Termination")]
    ndf['combo']=ndf['empl_id'].astype('str')+ndf['dept_id_job'].astype('str')
    ndf.effdt=pd.to_datetime(ndf.effdt_job)
    
    
    
    cols=["EMPLMT_SRCH_COR_EMPLID","EMPLMT_SRCH_COR_EMPL_RCD","JOB_EFFDT$0",
                 'JOB_ACTION$0',"JOB_ACTION_REASON$0","JOB_EXPECTED_END_DATE$0",
                 "CU_JOB_JR_CU_APPOINT_HRS$0"]
    
    if flag:
       listoftups=list(deletions[['empl_id','empl_rcd']].to_records(index=False))
       return(listoftups)
    effdict={i:ndf[ndf.combo==i].effdt_job.unique() for i in list(ndf.combo.unique())}
    rcddict={i:ndf[ndf.combo==i].empl_rcd.unique()[0] for i in list(ndf.combo.unique())}
    together['rcd']=together['combo'].apply(lambda x: rcddict[x] if x in rcddict.keys() else '')
    together['later']=together.combo.apply(lambda x: effdict[x][0] if x in effdict.keys() else  '')
    together['later']
    together['later']=pd.to_datetime(together['later'])
    #TODO fix this hardcoded clusterfuck, shane
    thisdf=together[together.date>together.later][~together.rcd.str.contains('',na=False)][together.paf_type.str.contains('Revision',na=False)]
    thisdf['action']='Data Change'
    thisdf=thisdf[['empl_id','rcd','date', 'action','paf_type','end_date','bgt_hrs']]
    listoftups=list(thisdf.to_records(index=False))
     
    
    #finding out if all titles are unique sets of letters
    #len([set(i) for i in df.jobcode_ld.unique()])==len(list(set([''.join(set(i)) for i in df.jobcode_ld.unique()])))
    #turns out they aren't.
    
    #convert paf_type column into simple action reason using apply statement and dict
    
    

    listofdicts=[]
    for tup in listoftups:
        tupdict={}
        for ix,i in enumerate(tup):
            if len(str(i))==29:
                i=datetime.strptime(str(i)[:10],'%Y-%M-%d').strftime('%M/%d/%Y')
            tupdict.update({cols[ix]:str(i)})
        listofdicts.append(tupdict)
    return(listofdicts)
    #create dictionary using dict expression, enumerate, and df call
    
    
    #and turning into records specifically for automating
if __name__=="__main__":
    filefolder=DIR
    listoftups=pr_data(filefolder,flag=True)
    listofdicts=pr_data(filefolder)