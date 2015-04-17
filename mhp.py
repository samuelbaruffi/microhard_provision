###################
#
# Microhard Configuration Script
#
# Usage:
# -r              : produce a report
# -n hostname     : change hostname to this name
# -i ip address   : use this ip address (default is 10.254.0.19)
# -u upload config: upload config file to microhard (default is ./)
# -s ssl          : set ssl to http (https)
# -p password     : password (default is admin)
#
# Ver 1.0 - April 2015 by Sam and John
#
#
###################

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import *
from bs4 import BeautifulSoup
from distutils.command.upload import upload
from _ast import Try

import time
import argparse
import json
from asyncio.tasks import sleep


class Reporter():        # Class to report on a device
    
    #Function to connect to a device using BeautifulSoup
    def connect(self, theurl, password, ssl):
        
        passman = HTTPPasswordMgrWithDefaultRealm()
        # this creates a password manager


        passman = HTTPPasswordMgrWithDefaultRealm()  # this creates a password manager

        passman.add_password(None, theurl, 'admin', password)
        # because we have put None at the start it will always
        # use this username/password combination for  urls
        # for which `theurl` is a super-url
        
	#if ssl == s:
              
        #else:
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

    #Function to generate a dictionary of information about the device
    def getInfo(self):
        values = ["Product Name","IMEI","Host Name","Build Version","SIM Number (ICCID)","Description","Hardware Version","Software Version"]
        
        dict = {value: self.findValue(value) for value in values}
        dict['Network'] = self.getNetworkStatus()
        dict['MAC Address'] = self.findValue("255.255.255.0")
        return(dict)
    
                
         #verify is result is unkown means not connected       
        if networkStatus == "Unknown":
            return('Not Connected')
        else:
            return(networkStatus)


    #Function to find to find the Network Status
    def getNetworkStatus(self):
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
            return('Not Connected')
        else:
            return(networkStatus)

    #Function to grab info off a device 
    def findValue(self, text):
        result = ''
        splitText = self.text.split('\n')
        for cnt,line in enumerate(splitText):
            if text in line:
                 result = splitText[cnt+1].strip()
                 break
        return result
    


class Configuration():   # Class to configure the device

    #f = open ('log.txt', 'a')

    #Function to return an open connection to a site in a browser
    def connect(self, site = 'http://admin:admin@10.254.0.19/'):
        p = webdriver.FirefoxProfile()
        p.set_preference('webdriver.log.file','/tmp/firefox_console')
        self.driver = webdriver.Firefox(p)
        self.driver.get(site)

    #Function to set the host name on a site that is open
    def setHostname(self, name):
        driver = self.driver
        hostname=name
        
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
    def upgradeFirmware(self,firmware="/Users/sambaruffi/git/microhard_provision/firmware.bin"):
        driver = self.driver
        print(firmware)
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
    
        #Reconfirming the "Restor" button
        uploadConfigRestoreButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("instconfig"))
        uploadConfigRestoreButtonEle.click()
        
        #sleep 60 seconds to upload the file
        time.sleep(60)
        
        
    #Function to close the connection to site that is open                                                           
    def tearDown(self):
        self.driver.quit()
    
    

def main2131():
    
    configURL = 'http://admin:admin@10.254.0.19'
    print(configURL)  # test
    siteConfig = Configuration() # create a Configuration() object called siteConfig
    siteConfig.connect(configURL) # connect to the configURL
    siteConfig.uploadConfigurationFile("/Users/sambaruffi/Desktop/IPsec_User_Guide.pdf")




def main():
    
    # create an ArgumentParser() Object (defined in the argparse library we imported)
    parser = argparse.ArgumentParser(description='Microhard Reporting and Configuation Utility')
    
    # Arguments:
    parser.add_argument('-r','--report',help='Return report',required=False,action='store_true' )
    parser.add_argument('-n','--nameChange',help='Change the Hostname to ...',required=False,default="")
    parser.add_argument('-i','--ip',help='Choose IP of device',required=False,default='10.254.0.19')
    parser.add_argument('-u,','--uploadconfig',help="Upload the config file",required=False,action='store_true')
    parser.add_argument('-p','--password',help="Set the password",required=False,default='admin')
    parser.add_argument('-s','--ssl',help='Set https',required=False,action='store_true')
    parser.add_argument('-f','--firmware',help='Upgrade Firmware',required=False,action='store_true')
    
    
    args = parser.parse_args()  # this variable is a dictionary of the arguments entered at the command line

    ssl = ''
    if args.ssl == True:
        ssl = 's'

    #Create URLz - we will pass this to connect() functions
    configURL = 'http' + ssl + '://admin:' + args.password + '@' + args.ip + '/'
    reportURL = 'http' + ssl + '://' + args.ip + '/cgi-bin/webif/system-info.sh'

    # -f
    if args.firmware == True:
        try:
            siteUpgrade = Configuration()
            siteUpgrade.connect(configURL)
            siteUpgrade.upgradeFirmware()
            siteUpgrade.tearDown()
            print('True')
        except Exception as e:
            print(e)
            siteUpgrade.tearDown()


    # -u
    if args.uploadconfig == True:
        file = '/support/microhard/microhard_provision/IPn4G.config'
        try:
            siteUpload = Configuration()
            siteUpload.connect(configURL)
            siteUpload.uploadConfigurationFile(file)
            time.sleep(20)
            siteUpload.tearDown()
            print('True')
        except Exception as e:
            print(e)
            
            
    # -r
    if args.report == True:  # If report (-r) arg was given, then return a report

        try:
            siteReport = Reporter() # Create object from Reporter() class
            siteReport.connect(reportURL, args.password, ssl) # Connect to URL
            report = siteReport.getInfo()
            print(json.dumps(report))
        except Exception as e:
            print(e)

    # -n ____
    if args.nameChange != "":
        
        try:
            siteConfig = Configuration() # create a Configuration() object called siteConfig
            siteConfig.connect(configURL) # connect to the configURL
            siteConfig.setHostname(args.nameChange) # set the Hostname
            siteConfig.tearDown() # close the session
            print('True')
        except Exception as e:
            print(e)
            siteConfig.tearDown()

if __name__=='__main__':main()

