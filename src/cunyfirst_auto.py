from time import sleep
from seltools import mydriver,main
from cunydatatools import jsrename
from selenium.webdriver.common.by import By


class cunyfirst(main):
    loginurl="https://home.cunyfirst.cuny.edu/oam/Portal_Login1.html"
    unfield="CUNYfirstUsernameH"
    pwfield="CUNYfirstPassword"
    submit="submit"
    def login(self):    #consider moving this to seltools and usising data_dist
        self.driver.get(self.loginurl)
        self.waitfillid(self.unfield,self.un)
        self.waitfillid(self.pwfield,self.pw)
        self.main_window = self.driver.current_window_handle
        self.waitid(self.submit)
    def route(self):
        self.driver.switch_to.window(self.main_window)  
        self.waitlink(self.cfmodule)
        self.driver.switch_to.window(self.driver.window_handles[-1])
    def loginnow(self):
        self.login()
        self.route()
    def pagecheck(self):
        if self.driver.title == 'CUNY Login':
            self.login()
    def parsehtml(self,x):
        #use this on pagesource to turn html into a list of strings
        #makes it easy to scan portions of long html for particular substrings
        #also allows looking at surrounding code of that instance using index position
        """
        Use this like `parsehtml(___.driver.page_source)`
        """
        x=x.replace(">","999999")
        x=x.replace("<","999999")
        x=x.replace(">","999999")
        x=x.split("999999")
        return(x)

#TODO rewrite functionality to leverage available keyboard shortcuts (quicker)
#TODO split off class files as they are realized
#TODO continue to build out cunyfirst() functionality to feed down to children
#TODO develop campus services class
#TODO develop HCM query class
#TODO develop customer relation manager class
#TODO talk to Budget about the possibility of doing their module (stretch goal)
#TODO develop student class (for shits and giggles, I assure you).

    
class pospages(hcm,main):
    def __init__(self, driver):
        self.driver=driver
        self.url="https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/MANAGE_POSITIONS.POSITION_DATA.GBL"    
        self.searchfield="POSITION_SRCH_POSITION_NBR"
        self.nav()
    """    
    def nav(self):
        self.outer_instance.nav(self.url,self.searchfield)
    def move(self,num):
        self.outer_instance.move(num)
    """
        
    field1="POSITION_SRCH_POSITION_NBR"
    search="#ICSearch"
    add_row="$ICField3$new$0$$0"
    save="#ICSave"
    
    def return_switch(self):
        try:
            self.driver.switch_to.frame('TargetContent')
        except:
            self.driver.switch_to.default_content()
            
    def update_pos(self,corr=None,activate=None,dt=None,newrt=None,dept=None,title=None,line=None,payserv=None,reason=None):
        if corr:
            if self.windowswitch("#ICCorrection",0):    
                self.waitid("#ICCorrection")
                self.wait_spin()
        else:
            if self.windowswitch(self.add_row,0):
                self.waitid(self.add_row)
                self.wait_spin()
                sleep(1)
        if dept:
            if self.windowswitch('POSITION_DATA_DEPTID$0',0):
                print('udpating department')
                try:
                    self.waitfillid('POSITION_DATA_DEPTID$0',dept)
                except:
                    self.return_switch()
                    self.waitfillid('POSITION_DATA_DEPTID$0',dept)
                self.wait_spin()
                self.okay2()
                self.return_switch()
        if newrt:
            if self.windowswitch('POSITION_DATA_REPORTS_TO$0',0):
                print('udpating reports to')
                try:
                    self.waitfillid('POSITION_DATA_REPORTS_TO$0',newrt)
                except:
                    self.return_switch()
                    self.waitfillid('POSITION_DATA_REPORTS_TO$0',newrt)
                self.wait_spin()
                self.okay2()
                self.return_switch()
        if dt:
            if self.windowswitch('POSITION_DATA_EFFDT$0',0):
                print('udpating date')
                try:
                    self.waitfillid('POSITION_DATA_EFFDT$0',dt)
                except:
                    self.return_switch()
                    self.waitfillid('POSITION_DATA_EFFDT$0',dt)
                self.wait_spin()
                self.okay2()
                self.return_switch()
            else:
                print('udpating date')
                self.return_switch()
                self.waitfillid('POSITION_DATA_EFFDT$0',dt)
                self.wait_spin()
                self.okay2()
                self.return_switch()
        if reason:
            if self.windowswitch('POSITION_DATA_ACTION_REASON$0',0):
                print('udpating updating reason')
                try:
                    self.waitfillid('POSITION_DATA_ACTION_REASON$0',reason)
                except:
                    self.return_switch()
                    self.waitfillid('POSITION_DATA_ACTION_REASON$0',reason)
                self.wait_spin()
                self.okay2()
                self.return_switch()
        if activate:
            if self.windowswitch("POSITION_DATA_EFF_STATUS$0",0):
                if self.dropdownitembyid("POSITION_DATA_EFF_STATUS$0")!='Active':
                    print('udpating Effective Status')
                    try:
                        self.dropdownselector("POSITION_DATA_EFF_STATUS$0",'Active')
                    except:
                        self.return_switch()
                        self.dropdownselector("POSITION_DATA_EFF_STATUS$0",'Active')
                    self.wait_spin()
            if self.windowswitch("POSITION_DATA_POSN_STATUS$0",0):
                print('udpating position status')
                if self.dropdownitembyid("POSITION_DATA_POSN_STATUS$0")!='Approved':
                    try:
                        self.dropdownselector("POSITION_DATA_POSN_STATUS$0",'Approved')
                    except:
                        self.return_switch()
                        self.dropdownselector("POSITION_DATA_POSN_STATUS$0",'Approved')
                    self.wait_spin()
        if self.windowswitch("ICTAB_1",0):
            print('switching tabs')
            self.waitid("ICTAB_1")
            sleep(1)
        if self.windowswitch("POSITION_DATA_UPDATE_INCUMBENTS$0",0):
            print('udpating incumbent checkbox')
            try:
                self.waitid("POSITION_DATA_UPDATE_INCUMBENTS$0")
            except:
                self.return_switch()
                self.waitid("POSITION_DATA_UPDATE_INCUMBENTS$0")
            self.okay2()
        sleep(1)
        self.simplesave()
        self.okay2()
    def mass_rt_upd(self,poslist,effdt,posnum):
        successlist=[]
        faillist=[]
        for i in poslist:   #gotta gather position numbers from CF to create poslist
            self.nav()
            try:
                self.openrecord("pos",[i])
                self.update_pos(newrt=posnum,dt=effdt,reason='RTC')
                successlist.append(i)
            except:
                faillist.append(i)
                pass
        print('Successes:')
        print(','.join(successlist))
        print('Failures')
        print(','.join(faillist))

class jobsummary(hcm,main):
    search=("#ICSearch")
    def __init__(self,driver):
        self.driver=driver
        self.url="https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/CU_E065_JOB_SUMMARY.CU_JOB_SUMMARY.GBL"
        self.searchfield="CU_JOB_SUM_SRCH_EMPLID"
    def survey(self):
        return(self.outer_instance.survey())
    def nav(self):
        self.outer_instance.nav(self.url,self.searchfield)
    
    def downloader(self,emplid):    #TODO modify to accept multiple values
        self.data_distribute({"CU_JOB_SUM_SRCH_EMPLID":f'{emplid}'})
        self.waitid(self.search)
        self.wait_spin()
        self.waitid("ICTAB_HIDE_29")
        sleep(1)
        self.waitid("WF_JOB_SUMM$hexcel$0")
        sleep(5)
        jsrename(emplid,download_dir)
        self.nav()

class reports(object):
    #TODO fill this out with all basic HCM reports
    #TODO Use code from CJR, either implemented in base class or lcoally
    def __init__(self, outer_instance):
        self.outer_instance = outer_instance
        self.driver=self.outer_instance.driver
    def run(self,searchbt,dt):
        self.waitid(searchbt)
        #if link, click link
        #insert dt in effective date field if exists
        #press run
        #press ok
        #wait preset period of time (or switch to another task)
        #press report manageer
        #waitspin
        #look for table containing report name "CURRENT DATA EXTRACT REPORT"
        #if found, click "CU_R1013"
        #waitid("URL$1")  IF the href ends in the filetype we're looking for, not "log"
    class cjr(object):
        url="https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/CU_HCM.CU_R1013.GBL"
            
def parse_hr_trans(df):
    df=df[(df.Action=="Termination")&(df['Action Reason']=='Mass System Termination')]    
    df['code']= df['Employee ID'].astype('str')+df['Empl RCD'].astype('str')
    return(df[['code']])


    
def frame_search(driver,path):
    framedict = {}
    for child_frame in driver.find_elements_by_tag_name('frame'):
        child_frame_name = child_frame.get_attribute('name')
        framedict[child_frame_name] = {'framepath' : path, 'children' : {}}
        xpath = '//frame[@name="{}"]'.format(child_frame_name)
        driver.switch_to.frame(driver.find_element_by_xpath(xpath))
        framedict[child_frame_name]['children'] = frame_search(framedict[child_frame_name]['framepath']+[child_frame_name])
        #do something involving this child_frame
        driver.switch_to.default_content()
        if len(framedict[child_frame_name]['framepath'])>0:
            for parent in framedict[child_frame_name]['framepath']:
                parent_xpath = '//frame[@name="{}"]'.format(parent)
                driver.switch_to.frame(driver.find_element_by_xpath(parent_xpath))
    return framedict

def find_all_iframes(driver):
    #TODO Improve this code. Still fails in CJR module in CF
    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    print(len(iframes))
    for index, iframe in enumerate(iframes):
        print(iframe.text)
        driver.switch_to.frame(index)
        find_all_iframes(driver)
        driver.switch_to.parent_frame()


if __name__ == "__main__":
    print("I'm pretty sure you meant to load one of this files' child classes.")