# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 17:17:21 2021

@author: shane
"""
from HCM_main import hcm
from seltools import mydriver,main
from datetime import datetime, timedelta
from time import sleep
import time
from CF_PR_datapipeline import pr_data



class jobpages(hcm,main):
    def __init__(self, driver):
        self.driver=driver
        self.url="https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/ADMINISTER_WORKFORCE_(GBL).JOB_DATA.GBL"
        self.searchfield="EMPLMT_SRCH_COR_EMPLID"
    
    field1="EMPLMT_SRCH_COR_EMPLID"
    field2="EMPLMT_SRCH_COR_EMPL_RCD"
    search="#ICSearch"
    navid="ICTAB_1"
    save="#ICSave"
    tabs=["ICTAB_0","ICTAB_1","ICTAB_2","ICTAB_3","ICTAB_4","ICTAB_5"]
    links=["DERIVED_HR_JOB_DATA_BTN1","DERIVED_HR_JOB_DATA_BTN2","DERIVED_HR_JOB_DATA_BTN3","DERIVED_HR_JOB_DATA_BTN4","DERIVED_CU_JOB_DATA_BTN"]
    
    def add_row(self):
        self.switch_tar()
        self.waitid('$ICField12$new$0$$0')
    def createdict(self,process_item):
        if type(process_item)=='list':
            empldict={}    
            empldict["EMPLMT_SRCH_COR_EMPLID"]=process_item[2]
            empldict["EMPLMT_SRCH_COR_EMPL_RCD"]=process_item[5]
            empldict["JOB_EFFDT$0"]=process_item[0]
            empldict['JOB_ACTION$0']='Data Change'
            empldict["JOB_ACTION_REASON$0"]="Revision"
            empldict["JOB_EXPECTED_END_DATE$0"]=process_item[6]
            empldict["CU_JOB_JR_CU_APPOINT_HRS$0"]=process_item[7]
        else:
            objlist=["EMPLMT_SRCH_COR_EMPLID","EMPLMT_SRCH_COR_EMPL_RCD","JOB_EFFDT$0",
                     'JOB_ACTION$0',"JOB_ACTION_REASON$0","JOB_EXPECTED_END_DATE$0",
                     "CU_JOB_JR_CU_APPOINT_HRS$0"]
            empldict={obj:process_item[obj] for obj in objlist}
        return(empldict)   

    def deletion_new(self):
        #step 1 - go into correction mode
        self.switch_tar()
        self.waitid("#ICCorrection")
        self.cf_save(1) #deprecated wait_spin for cf_save(1)
        #step 2 - remove position number
        self.switch_tar()
        y=self.getvals("JOB_POSITION_NBR$0")
        if len(y)>2:
            self.data_distribute({"JOB_POSITION_NBR$0":''})
        self.cf_save(0)
        #step 3 - remove end date
        self.switch_tar()
        z=self.getvals("JOB_EXPECTED_END_DATE$0")
        if len(z)>2:
            self.data_distribute({"JOB_EXPECTED_END_DATE$0":''})
            self.cf_save(0)
        #step 4 - change effective date
        self.switch_tar()
        x=self.getvals("JOB_EFFDT$0")
        #changing the effective date to yesterday should work in most cases.
        x=(datetime.strptime(x, "%m/%d/%Y")-timedelta(days=1)).strftime("%m/%d/%Y")
        self.data_distribute({"JOB_EFFDT$0":x})
        self.cf_save(1)
        self.cf_save(0)
        #step 5 - time to change action and reason
        self.switch_tar()
        x=self.dropdownitembyid("JOB_ACTION$0")
        y=self.dropdownitembyid("JOB_ACTION$0")
        if x!="Data Change":
            term="Data Change"
        else:
            term="Reappointment"
        while x==y:
            print("attempting to update action")
            self.data_distribute({"JOB_ACTION$0":term})
            y=self.dropdownitembyid("JOB_ACTION$0")
            self.cf_save(1)
        print('action updated')
        termdict={"Data Change":"Revision","Reappointment":"Reappointment"}
        term=termdict[term]
        #step -6 changing reason
        self.cf_save(1) #wait_spin
        self.switch_tar()
        x=self.dropdownitembyid("JOB_ACTION_REASON$0")
        y=self.dropdownitembyid("JOB_ACTION_REASON$0")
        while y==x:
            print('attempting to update reason')
            self.data_distribute({"JOB_ACTION_REASON$0":term})
            y=self.dropdownitembyid("JOB_ACTION_REASON$0")
            self.cf_save(1)
        print('reason updated')
        #changing to Data Change/ Revision ALWAYS returns end date, thus remove
        self.switch_tar()
        z=self.getvals("JOB_EXPECTED_END_DATE$0")
        if len(z)>2:
            self.data_distribute({"JOB_EXPECTED_END_DATE$0":''})
            self.cf_save(0)
        #finally, remove record.
        self.switch_tar()
        self.waitid("$ICField12$delete$0$$0")
        self.cf_save(1)
        self.cf_save(0)

    def open_this(self,empldict):
        self.data_distribute(empldict)
        self.waitid(self.search)
        self.wait_spin()
        try:
            self.driver.find_element_by_id("SEARCH_RESULT1").click()
            self.wait_spin()
        except:
            pass
    def massdeletion(self,obj):
        if type(obj)!=list:
            for i in obj.code.values:
                sleep(1)
                self.open_record('job',[i[:-1],i[-1:]])
                self.wait_spin()
                if self.gettext("JOB_EMPL_STATUS$0")=="Terminated":
                    self.deletion()
                self.nav() 
        else:
            for i in obj:
                sleep(1)
                self.openrecord('job',[x for x in i])
                self.wait_spin()
                if self.gettext("JOB_EMPL_STATUS$0")=='Terminated':
                    self.deletion()
                self.nav()
                
    def random_click(self):     #doesn't $&@!ing work.
        self.driver.execute_script('el = document.elementFromPoint(440, 120); el.click();')

    def reappointment(self,dt=None,ation=None,reason=None,appthrs=None,prohrs=None):
        if dt:
            print("do soething here shane")
    
    def return_from(self,empldict):
        self.add_row()
        self.cf_data_distribute(empldict)
        self.cf_save[0]
        
    def return_switch(self):
        try:
            self.driver.switch_to.frame('TargetContent')
        except:
            self.driver.switch_to.default_content()    
    
    def revision(self,empldict):
        #TODO speed datadistribute by using page-specific data
        #TODO make visiting all pages mandatory if ther eis data from them
        empldict1=[v for k,v in empldict.items() if k in ["EMPLMT_SRCH_COR_EMPLID","EMPLMT_SRCH_COR_EMPL_RCD"]]
        empldict1=[str(max([int(x) for x in empldict1])),str(min([int(x) for x in empldict1]))]
        self.openrecord('job',empldict1)
        if self.getvals("JOB_EFFDT$0")==empldict["JOB_EFFDT$0"] and self.gettext("JOB_ACTION_DT$0")==datetime.now().strftime('%m/%d/%Y'):
            #unfortunately, this will prevent us from loading anything same dated
            #TODO fix this part of the function. Does require sequence validation.
            self.nav()
            return()
        elif datetime.strptime(self.getvals("JOB_EFFDT$0"),'%m/%d/%Y')>datetime.strptime(empldict["JOB_EFFDT$0"],'%m/%d/%Y'):
            self.nav()
            return()
        if self.gettext('JOB_EMPL_STATUS$0') == "Short Work Break":
            ding=self.getvals("JOB_EFFDT$0")
            dong=self.getvals("JOB_EFFSEQ$0")
            empldict,empldict2=self.swbdict(empldict,ding,dong)
            self.return_from(empldict2)
        self.add_row()
        #source=self.driver.page_source
        self.data_distribute(empldict)
        self.cf_save(1)
        try:
            self.cf_save(1)
            self.switch_tar()
            self.waitid("DERIVED_CU_JOB_DATA_BTN")
        except:
            self.cf_save(1)
            sleep(1)
            self.waitid("DERIVED_CU_JOB_DATA_BTN")
            sleep(1)
        self.data_distribute(empldict)
        self.cf_save(0)
        sleep(1)
        self.nav()
        
    def swbdict(empldict,datething,seq):
        if empldict['JOB_EFFDT$0']==datething:
            seq=str(int(seq)+1)
        else:
            seq="0"
        empldict2={**empldict,**{"JOB_EFFSEQ$0":seq}}
        empldict2['JOB_ACTION$0']='Return From Work Break'
        empldict2["JOB_ACTION_REASON$0"]='Return From Work Break'
        seq=str(int(seq)+1)
        empldict={**empldict,**{"JOB_EFFSEQ$0":seq}}
        return(empldict,empldict2)

    #below are fields in the Job Data area pages for easy reference.
    #TODO convert to dictionary. Unnecessary class designation just to store info
    class workloc:
        effdt="JOB_EFFDT$0"
        seq="JOB_EFFSEQ$0"
        hrstatus="JOB_HR_STATUS$0"
        prstatus="JOB_EMPL_STATUS$0"
        action="JOB_ACTION$0"
        reason="JOB_ACTION_REASON$0"
        expend="JOB_EXPECTED_END_DATE$0"
        position="JOB_POSITION_NBR$0"
        date_created="JOB_ACTION_DT$0"
        indicator="JOB_JOB_INDICATOR$0"
        add_row="$ICField12$new$0$$0"
        del_row="$ICField12$delete$0$$0"
        include_hist="#ICUpdateAll"
        correct_hist="#ICCorrection"
        find_row="$ICField12$hfind$0"
        notes="DERIVED_HR_NP_HR_NP_INVOKE_ICN$0"
    class notes:
        add_note="DERIVED_HR_NP_HR_NP_ADD_PB"
        note_type="HR_NP_NOTE_CU_NOTE_TYPE$0"
        subject="HR_NP_NOTE_HR_NP_SUBJECT$0"
        text="HR_NP_NOTE_HR_NP_NOTE_TEXT$0"
        save="DERIVED_HR_NP_HR_NP_SAVE_PB"
    class jobinfo:
        empl_class="JOB_EMPL_CLASS$0"
        officer="JOB_OFFICER_CD$0"
        reports_to="JOB_REPORTS_TO$0"
        jobcode="JOB_JOBCODE$0"
        fte_actual="JOB_ADDS_TO_FTE_ACTUAL$0"
        ft_status="JOB_FULL_PART_TIME$0"
        reg_temp="JOB_REG_TEMP$0"
    class joblabor:
        barg_unit="JOB_BARG_UNIT$0"
        labor_arg="JOB_LABOR_AGREEMENT$0"
        union_dt="JOB_ENTRY_DATE$0"
        union_fee="JOB_PAY_UNION_FEE$0"
        union_seniority="JOB_UNION_SENIORITY_DT$0"
        empl_category="JOB_EMPL_CTG$0"
        union_code="JOB_UNION_CD$0"
        recalc_seniority="DERIVED_HR_LBR_HR_SNR_DT_DEF_BTN$0"
    class payroll:
        pay_system="JOB_PAY_SYSTEM_FLG$0"
        paygroup="JOB_PAYGROUP$0"
        holiday="JOB_HOLIDAY_SCHEDULE$0"
        fica_status="JOB_FICA_STATUS_EE$0"
    class salary_plan:
        plan="JOB_SAL_ADMIN_PLAN$0"
        refresh_plan="DERIVED_HR_REFRESH_BTN$0"
        grade="JOB_GRADE$0" 
        grade_refresh="DERIVED_HR_REFRESH_BTN$12$$0"
        step="JOB_STEP$0"
        grade_entry_dt="JOB_GRADE_ENTRY_DT$0"
        step_entry_dt="JOB_STEP_ENTRY_DT$0"
    class compensation:
        comp_rt_fd="JOB_COMPRATE$0"
        comp_freq="JOB_COMP_FREQUENCY$0"
        default_pay="DERIVED_HR_CMP_DFLT_COMP_BTN$0"
        rate_code="COMPENSATION_COMP_RATECD$0"
        comp_rate="COMPENSATION_COMPRATE$0"
        calc_comp="DERIVED_HR_CMP_CALC_COMP_BTN$0"
    class cunyinfo:
        appt_hrs="CU_JOB_JR_CU_APPOINT_HRS$0"
        pro_hrs="CU_JOB_JR_CU_PROF_HRS$0"
        pay_percent="CU_JOB_JR_CU_LEAVE_PER_PAY$0"
    class emp_data:
        override_orig_dt="PER_ORG_INST_ORIG_HIRE_OVR$0"
        orig_dt="PER_ORG_INST_ORIG_HIRE_DT$0"
    



#TODO update main to be interruptable without data loss from CF_PR_DP
def main(USERNAME,PASSWORD,download_dir=None,tups=None,dicts=None):
    if download_dir:
        download_dir=download_dir
    else:
        download_dir="C:\\insert\\default\\folder\\here"
    driver=mydriver.setupbrowser(mydriver(download_dir))
    home=hcm(driver,un=USERNAME,pw=PASSWORD)
    home.loginnow()
    job=jobpages(home.driver)
    job.nav()
    if tups or dicts:
        listoftups=tups
        listofdicts=dicts
    else:
        filefolder=download_dir
        listoftups=pr_data(filefolder,flag=True)    #these are deletions
        listofdicts=pr_data(filefolder) #these are additions
    #currently this process only supports data from PR-Assist
    #TODO bridge AEMS into pr_data process or design duplicate
    for ix,i in enumerate(listoftups):
        try:
            job.nav()
            job.openrecord("job",i)
            job.deletion_new()
            print(f'record {ix} complete.')
        except:
            print(f'problem with record {ix}')
            job.nav()
    
    for ix,i in enumerate(listofdicts):
        start_time = time.time()
        try:
            job.revision(i)
            print(f'completing item {ix}.')    
        except:
            print(f'error with item {ix}')
            job.nav()
        print("Currently at : %s seconds using given test case" % (time.time() - start_time))
    job.driver.quit()   #using quit instead of close because 2 windows.

def optional_main(USERNAME,PASSWORD,download_dir=None,tups=None,dicts=None):
    if download_dir:
        download_dir=download_dir
    else:
        download_dir="C:\\insert\\default\\folder\\here"
    driver=mydriver.setupbrowser(mydriver(download_dir))
    home=hcm(driver,un=USERNAME,pw=PASSWORD)
    home.loginnow()
    job=jobpages(home.driver)
    job.nav()
    if dicts:
        listofdicts=dicts
    else:
        listofdicts=[]
    for ix,i in enumerate(listofdicts):
        start_time = time.time()
        try:
            job.revision(i)
            print(f'completing item {ix}.')    
        except:
            print(f'error with item {ix}')
            job.nav()
        print("Currently at : %s seconds using given test case" % (time.time() - start_time))
    job.driver.quit()   #using quit instead of close because 2 windows.

if __name__=='__main__':
    #main(USERNAME,PASSWORD,download_dir=DIR)
    optional_main(USERNAME,PASSWORD,download_dir=DIR,dicts=listofdicts)