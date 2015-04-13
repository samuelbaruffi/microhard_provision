###################
#
# Microhard Configuration Script
#
# Usage:
# -r            : produce a report
# -n hostname   : change hostname to this name
# -i ip address : use this ip address (default is 10.254.0.51)
#
#
#
###################

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import unittest
import time
from urllib.request import *
import argparse
from distutils.command.upload import upload
from _ast import Try


class Reporter():
    
    def connect(self, theurl, username='admin', password='admin'):
        
        passman = HTTPPasswordMgrWithDefaultRealm()
        # this creates a password manager


        passman = HTTPPasswordMgrWithDefaultRealm()  # this creates a password manager

        passman.add_password(None, theurl, username, password)
        # because we have put None at the start it will always
        # use this username/password combination for  urls
        # for which `theurl` is a super-url
        
        authhandler = HTTPBasicAuthHandler(passman) # create the AuthHandler
        opener = build_opener(authhandler)
        
        install_opener(opener)
        # All calls to urllib2.urlopen will now use our handler
        # Make sure not to include the protocol in with the URL, or
        # HTTPPasswordMgrWithDefaultRealm will be very confused.
        # You must (of course) use it when fetching the page though.
        
        #pagehandle = urlopen(theurl)
        # authentication is now handled automatically for us
        
        page = urlopen(theurl).read()
        soup = BeautifulSoup(page)
        self.text = soup.get_text() 

    def getNetworkStatus(self):
        #To find to find the Network Status
        counter = 0
        networkStatus = ''
        splitText = self.text.split('\n')
        for cnt,line in enumerate(splitText):
            if counter == 1 and 'Network' in line:
                networkStatus = splitText[cnt+1].strip()
                break
            elif 'Network' in line:
                counter+=1
                
         #verify is result is unkown means not connected       
        if networkStatus == "Unknown":
            print("Not Connected")
        else:
            print("Network is: " + networkStatus)
        

    def getInfo(self):
        #get Product Name and IMEI
        value = ["Product Name","IMEI","Host Name","Build Version"]
       

        productName = self.findValue(value[0])
        imei = self.findValue(value[1])
        hostName = self.findValue(value[2])
        buildVersion = self.fo


        print (value[0], ":", productName)
        print (value[1], ":", imei)
        print (value[2], ":", hostName)
        print (value[3], ":", hostName)
      
            

    #function to find info 
    def findValue(self, text):
        result = ''
        splitText = self.text.split('\n')
        for cnt,line in enumerate(splitText):
            if text in line:
                 result = splitText[cnt+1].strip()
                 break
        return result
    

        
# class LoginTest(unittest.TestCase):
class Configuration():

    #f = open ('log.txt', 'a')

    #Function to return an open connection to a site in a browser
    def connect(self, site = 'http://admin:admin@10.254.0.51/'):
        p = webdriver.FirefoxProfile()
        p.set_preference('webdriver.log.file','/tmp/firefox_console')
        self.driver = webdriver.Firefox(p)
        self.driver.get(site)

    #Function to set the host name on a site that is open
    def setHostname(self, name):
        driver = self.driver
        hostname=name
        firmware = "/Users/sambaruffi/Downloads/IPn4G-v1_1_0-r1086-1.bin"
        
        #Change to the Settings tab in a Microhard
        settingButtonXpath = "//a[@href='/cgi-bin/webif/system-settings.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        #Change Hostname Field
        hostnameFieldXpath = "//input[@name='hostname']"
        hostanmeFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(hostnameFieldXpath))
        hostanmeFieldElement.clear()
        hostanmeFieldElement.send_keys(hostname)
        
        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()
    
    #Function to upload and upgrade firmware to a set that is open
    def upgradeFirmware(self):
        driver = self.driver
        #Move to Maintanence Page
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        
        #upload the file
        uploadButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("upgradefile"))
        uploadButtonEle.send_keys(firmware)
        
        #click upgrade 
        upgradeButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("upgrade"))
        upgradeButtonEle.click()
        
        #sleep for 10 minutes while upgrade
        time.sleep(600)
    
    #Function to upload configuration file
    def uploadConfigurationFile(self,configurationFilePath):
        driver = self.driver
        
        #go to Maintanence window
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        
        #upload the path to the file 
        uploadConfigButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("configfile"))
        uploadConfigButtonEle.send_keys(configurationFilePath)
        
        #click the "Restore" button
        uploadConfigConfirmButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("chkconfig"))
        uploadConfigConfirmButtonEle.click()
    
        
    #Function to close the connection to site that is open                                                           
    def tearDown(self):
        self.driver.quit()
    
    
    
    
    
# if __name__=='__main__':
#      unittest.main()            

# LoginTest().setUp().test_Login()


def main33():
    
    configURL = 'http://admin:admin@10.254.0.51'
    print(configURL)  # test
    siteConfig = Configuration() # create a Configuration() object called siteConfig
    siteConfig.connect(configURL) # connect to the configURL
    siteConfig.uploadConfigurationFile("/Users/sambaruffi/Desktop/IPsec_User_Guide.pdf")




def main    ():
    
    # create an ArgumentParser() Object (defined in the argparse library we imported)
    parser = argparse.ArgumentParser(description='Microhard Reporting and Configuation Utility')
    
    
    
    # use the add_argument() function to add kinds of  arguments to the parser object
#     parser.add_argument('-r','--report',help='Return report',required=False,action='store_true')
#     parser.add_argument('-n','--nameChange',help='Change the Hostname to ...',required=False,default="")
#     parser.add_argument('-i','--ip',help='IP of device',required=False,default='10.254.0.51')
#     parser.add_argument('-u,','--uploadconfig',help="Upload the config file",required=True,default="")

    parser.add_argument('-r','--report',help='Return report',required=False,action='store_true' )
    parser.add_argument('-n','--nameChange',help='Change the Hostname to ...',required=False,default="")
    parser.add_argument('-i','--ip',help='IP of device',required=False,default='10.254.0.51')
    parser.add_argument('-u,','--uploadconfig',help="Upload the config file",required=False,action='store_true')


    args = parser.parse_args()  # this variable is a dictionary of the arguments entered at the command line

    print(args.report)

    if args.report == True:  # If report (-r) arg was given, then return a report
        #Create URL for reporting  - we will pass this to connect() function in Reporter class
        reportURL = "http://" + args.ip + "/cgi-bin/webif/system-info.sh"
        print("Using this URL to connecto to the device:  " + reportURL  + "\n") # 

        siteReport = Reporter() # Create object from Reporter() class
        siteReport.connect(reportURL) # Connect to URL
        siteReport.getInfo()
        siteReport.getNetworkStatus()
        
    print("\n\n\n")    
    print("done report")  #test    

    if args.nameChange != "":
        configURL = 'http://admin:admin@' + args.ip + '/'
        print(configURL)  # test

        siteConfig = Configuration() # create a Configuration() object called siteConfig
        siteConfig.connect(configURL) # connect to the configURL
        siteConfig.setHostname(args.nameChange) # set the Hostname
        siteConfig.tearDown() # close the session
    
    print("done script")

if __name__=='__main__':main()

