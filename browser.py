x = "C://Users//milap/Downloads/edgedriver_win64 (1)/msedgedriver.exe"

import handle_kepacha
import time
import user_deatails as user
import constants as c

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Edge(service=Service(x))
driver.maximize_window()

driver.get("https://www.irctc.co.in/nget/train-search")



def modifypath(path,value,location=77):
    ##SL,DATE,BOOKNOW=location 77
    ##passenger = 117
    ls=list(path)
    ls[location]=str(value)
    return "".join(ls)


class webelement:
    '''
    using xpath we create webelement and than do various things.
    '''
    def __init__(self,xpath):
        #creates an instance of webelement using xpath
        #self.name is a driver welelement instance
        self.name=driver.find_element(by='xpath',value=xpath)
        self.xpath=xpath
        self.txt=self.name.text
        
    def click(self):
        self.name.click()
    
    def clearinput(self):
        self.name.clear()
    
    def send(self,data):
        self.name.send_keys(data)
    
    def select(self,value):
        Select(self.name).select_by_value(value)
        

def clickOnRekepacha(xpath):
    '''
    waits until rekepacha button element appears then clicks it.
    '''
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,xpath)))
    refreshbtnelement = driver.find_element(By.XPATH,xpath)
    try:
        driver.execute_script("arguments[0].click()", webelement(c.re_kepacha_xpath).name)
    except:
        print("something different")

def save_kepacha2():
    try:
        save_kepacha()
    except:
        WebDriverWait(driver,10).until(EC.presence_of_element_located(By.XPATH,c.kepacha2_img_xpath))
        myimgelement=driver.find_element(by='xpath',value=c.kepacha2_img_xpath)
        with open("kepacha.png") as k:
            while True:
                try:
                    k.write(myimgelement.screenshot_as_png)
                except:
                    time.sleep(1)
                else:
                    break

def save_kepacha():

    '''saves kepacha in a file called kepacha.png'''

    with open('kepacha.png','wb') as k:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"nlpCaptchaImg")))
        myimgelement=driver.find_element(by='id',value="nlpCaptchaImg")
        while True:
            try:
                k.write(myimgelement.screenshot_as_png)
            except:
                time.sleep(1)
            else:
                break



def justwait(xpath):
    '''
    waits 20 seconds for an element to appear
    '''
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,xpath)))

def do(xpath,fill_data='',wait=True,clearinput=False,click=False,select=False,send=False):
     
    #FIRST we should wait before creating an instance of of our class
    time=20
    if wait == True:
        #visibility_of_element_located(locator)
        #presence_of_element_located()
        #element_to_be_clickable()
        WebDriverWait(driver,time).until(EC.presence_of_element_located((By.XPATH,xpath)))
        WebDriverWait(driver, time).until(EC.element_to_be_clickable((By.XPATH,xpath)))
        
    #create webelement instance by xpath+
    element = webelement(xpath)
    
    if click == True:
        element.click()
    
    if clearinput == True:
        element.clearinput()
    if select == True:
        element.select(fill_data)
        
    if send == True:
        element.send(fill_data)

def get_ourdivision(train_no):
    '''
    input : train no
    returns :In which division of search results our desired train is located
    '''
    j=1
    while True:
        newxpath=modifypath(c.train_name_xpath,str(j))
        try:
            justwait(newxpath)
            y=webelement(newxpath).name.text
            print(y)
            if int(y[-6:-1]) == train_no:
                our_division = j
                break
        except:
            # j-1 total trains
            break
        j+=1
    #while loop ended
    return our_division
###CLICK __OK____
do(c.ok_btn_xpath,click=True)
    
##Now we'll login

def login():
    
    while True:
        do(c.login_btn_xpath,click=True) #clicks on login

        do(c.unamebox_xpath,fill_data=user.Username,send=True)
        do(c.passbox_xpath,fill_data=user.passwd,send=True)

        #kepacha business starts from here...
        #cliks on rekepacha button

        clickOnRekepacha(c.re_kepacha_xpath)
        save_kepacha()

        kepacha_answer=handle_kepacha.solve_kepacha()
        do(c.first_kepacha_box_xpath,fill_data=kepacha_answer,send=True)

        do(c.signinbtn_xpath,click=True)

        #TO verify if  we've really signed in!
        #otherwise maybe captcha erroe so we do this again
        try:
            WebDriverWait(driver,10).until_not(EC.text_to_be_present_in_element((By.XPATH,c.invalid_kapacha_xpath),"Invalid Captcha"))
            break
        except:
            print("Login Error!")
            
#login_success!    
    
##implicit wait 3 sec to load new things
driver.implicitly_wait(3)
##step 1 is completed now###


##Now we shall fill journey details:

def fill_journey_details():
    '''
    Filling train date ,class,quote,from and to station
    '''

    do(c.train_class_xpath,click=True)

    do(c.sl_class_xpath,click=True)

    do(c.booking_type_xpath,click=True)

    do(c.booking_tatkal_xpath,click=True)


    date_box = webelement(c.date_xpath).name

    date_box.clear()
    time.sleep(1)
    date_box.click()
    time.sleep(1)
    date_box.send_keys("26/07/2022")
    time.sleep(1)
    date_box.send_keys(Keys.TAB + Keys.TAB + Keys.TAB + Keys.ENTER)


    do(c.tobox_xpath,fill_data=user.to_station,send=True,clearinput=True)

    do(c.frombox_xpath,fill_data=user.from_station,send=True,clearinput=True)

    do(c.search_btn_xpath,click=True)
    ###need to check here again if we've really moved onto next page
    #and no error message is there

####page 1 over here#####
#waiting 3 sec to load new page
driver.implicitly_wait(3)

####page 2 starts###
train_no=20908

def select_train():
    '''
    Selects train by looking at search results and then modifying xpath accordingly
    by iterating our divisions
    to see if our train no matches with which division
    '''

    our_division=get_ourdivision(train_no)

    #Now we need to modify our xpath's 
    # For clicking on SLEEPER--> DATE - AVAILABLE--->BOOK NOW!
    ## HERE we have to add functionality to check if tickets are available or not!
    ##tatkal things will be done here later :)

    page2 = [c.page2_sl_xpath,c.page2_available,c.page2_booknow_xpath]
    page2_latest=[]

    for i in page2:
        page2_latest.append(modifypath(i,our_division))


    for j in page2_latest:
        do(j,click=True)
    
    ##Click on I Agree
    do(c.iagree,click=True)

##PAGE 2 OVER HERE ###
##waiting 3 sec to load new page
driver.implicitly_wait(3)


### NOW : PAGE 3  ####
## Now we fill passenger details..
def fill_passenger_details():
    '''
    fills passenger details
    '''
    NO_OF_PASSENGERS=1

    ##clicks on add new passenger "No.of.passenger-1" times
    for i in range(NO_OF_PASSENGERS-1):
        newxpath=modifypath(c.add_passenger_xpath,i+2,location=117)
        do(newxpath,click=True)

    ##there are four details fo fill up for every passenger name,gender,age,pref

    p1list = [c.passengername_xpath,c.pass_gender_xpath,c.pass_age_xpath,c.pass_pref_xpath]

    do(p1list[0],fill_data=user.passenger_name,send=True)

    do(p1list[1],fill_data='M',select=True)

    do(p1list[2],fill_data='22',send=True)

    do(p1list[3],fill_data='SL',select=True)


    ###HERE NUMBER on which ticket details is to be sent shoulf be filled
    # 
     
    do(c.pass_mobile_xpath,fill_data='8141377182',send=True)

    ###TWO payment options we have 1)upi 2)cards,wallets,etc..

    do(c.upi_option_radiobtn_xpath,click=True)

    do(c.continue_Btn_xpath,click=True)

##page 3 got over upon clicking continue button

driver.implicitly_wait(3)
###page 4 starts###

def page4():
    #it has kepacha and then just clicking continue button
    while True:
        clickOnRekepacha(c.p4_rekepacha_btn_xpath)
        save_kepacha()

        kepacha_answer=handle_kepacha.solve_kepacha()
        do(c.p4_kepacha_box_xpath,fill_data=kepacha_answer,send=True)

        do(c.signinbtn_xpath,click=True)

        #TO verify if  we've really signed in!
        #otherwise maybe captcha erroe so we do this again
        try:
            WebDriverWait(driver,3).until_not(EC.text_to_be_present_in_element((By.XPATH,c.p4_error_popup_xpath),"Invalid Captcha"))
            break
        except:
            print("Captcha error in page 4!")
    
    #while loop ended
    do(c.p4_continue_btn_xpath,click=True)
#page4 ends here
#waits for 3 seconds to load payment page
#it ussaly takes time to load this page
driver.implicitly_wait(4)
##page 5##

def do_payment():
    '''
    clicks on 
    BHIM --->POWERED BY PAYTM --->UPI JavaSc BOX--->
    fills UPI-ID--->VERIFY--->PAY XXXX Rs.
    '''

    do(c.bhim_xpath,click=True)

    do(c.poweredbypaytm_xpath,click=True)

    do(c.payandbook_xpath,click=True)

    do(c.upi_javascript_box_xpath,click=True)

    do(c.upi_box_xpath,fill_data="8141377182@ybl",send=True)

    do(c.verify_vpa_xpath,click=True)

    do(c.pay_button_xpath,click=True)

