from seltools import main
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