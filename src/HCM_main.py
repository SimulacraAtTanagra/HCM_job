# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 17:14:30 2021

@author: shane
"""
from cunyfirst_auto import cunyfirst
from seltools import mydriver
from time import sleep

class hcm(cunyfirst):
    def __init__(self,driver,un=None,pw=None):
        self.driver=driver 
        if un:
            self.un=un
        else:
            self.un=input("Please enter your username.\n")
        if pw:
            self.pw=pw
        else:
            self.pw=input("Please enter your password.\n")
        
    cfmodule="Human Capital Management"
    
    def nav(self):
        for i in range(30):
            if self.driver.execute_script('return document.readyState;')!="complete":
                sleep(1)
                pass
            else:
                self.driver.get(self.url)
                sleep(1)
                if self.driver.execute_script('return document.readyState;')!="complete":
                    sleep(1)
                    pass
                else:
                    sleep(1)
                    if hasattr(self,'searchfield'):
                        self.switch_tar()
                        self.waitid(self.searchfield)
                    return(True)
    
    def swtich(self):
        self.waitid(self.navid)

    def move(self,num): #deprecate this once we have a dict way to navigate tabs
        self.waitid(self.links[num])
        self.wait_spin() 
    def createjob(self):
        return(hcm.jobpages(self,mydriver))
    def createpos(self):
        return(hcm.pospages(self))
    def createjs(self):
        return(hcm.jobsummary(self))
        
    def survey(self):
        pagelist=[]
        pagelist.append(self.driver.page_source)
        for i in range(6):
            try: 
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(i+1)
                pagelist.append(self.driver.page_source)
            except:
                pass
        return(pagelist)
    def survey2(self):
        pagelist=[]
        pagelist.append(self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML"))
        for i in range(6):
            try: 
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(i+1)
                pagelist.append(self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML"))
            except:
                pass
        return(pagelist)
    def proceed_check(self):
        while True:
            a=('visible' in [self.save_flag(self.save_check())])
            try:
                self.return_switch()
            except:
                self.okay2()
            b=self.spinner()
            try:
                self.return_switch()
            except:
                self.okay2()
            c=self.windowswitch("ICOK",0)
            try:
                self.return_switch()
            except:
                self.okay2()
            d=self.windowswitch("ALERTOK",0)
            if a==False and b==False and c==False and d==False:
                return(True)
                break
            else:
                print('waiting to complete last action')
                print([i[0] for i in [(name,value) for  name, value in locals().items()] if i[1]!=False])
                self.wait_spin()
                self.okay2()
                
    def close_pop(self):
        if len(self.driver.window_handles)>2:
            self.driver.switch_to.window(driver.window_handles[-1])
            self.cf_okay()
            self.driver.switch_to.window(driver.window_handles[-1])
            self.switch_tar()
            if "Log in with" in self.driver.page_source:
                self.login()