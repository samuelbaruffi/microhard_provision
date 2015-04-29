from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import re
import time

class configgerer():

    def connect(self, configURL, ip):
        self.configURL = configURL
        self.ip = ip
        print(self.configURL)
        p = webdriver.FirefoxProfile()
        p.set_preference('webdriver.log.file','/tmp/firefox_console')
        self.driver = webdriver.Firefox(p)
        self.driver.get(self.configURL)

    def disconnect(self):
        self.driver.quit()

    def getMac(self):
        driver = self.driver
        settingButtonXpath = "//a[@href='/cgi-bin/webif/system-info.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        return(self.driver.find_element_by_xpath("//div[@id='content']/div[3]/table[2]/tbody/tr[3]/td[4]").text)

    def getFirmware(self):
        driver = self.driver
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 360).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        return(self.driver.find_element_by_xpath("//div[@id='content']/div/table[2]/tbody/tr[2]/td[4]").text)

    def uploadConfig(self,configurationFilePath):
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
    
        #Reconfirming the "Restore" button
        uploadConfigRestoreButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name("instconfig"))
        uploadConfigRestoreButtonEle.click()


    def setHostname(self, name, desc):
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
        
        fieldXpath = "//input[@name='description']"
        fieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(fieldXpath))
        fieldElement.clear()
        fieldElement.send_keys(desc)

        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()

    def setDesc(self, name):
        driver = self.driver
        desc=name
        print(desc)
        print("Change to the Settings tab in a Microhard")
        settingButtonXpath = "//a[@href='/cgi-bin/webif/system-settings.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        print("Change Hostname Field")
        fieldXpath = "//input[@name='description']"
        fieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(fieldXpath))
        fieldElement.clear()
        fieldElement.send_keys(desc)
        
        print("Submit the change, like a commit")
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()

    def setSSID(self, name):
        driver = self.driver
        ssid=name
        
        #Change to the Wireless tab
        wirelessButtonXpath = "Wireless"
        wirelessElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_link_text(wirelessButtonXpath))
        wirelessElement.click()
        
        #Change to the Settings tab in a Microhard
        settingButtonXpath = "//a[@href='/cgi-bin/webif/wireless-wlan0.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        #Change Hostname Field
        ssidFieldXpath = "//*[@id='ssid_0']"
        ssidFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(ssidFieldXpath))
        ssidFieldElement.clear()
        ssidFieldElement.send_keys(ssid)
        
        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()

    def setRadiusID(self, name):
        driver = self.driver
        radiusID=name
        
        #Change to the Wireless tab
        wirelessButtonXpath = "Wireless"
        wirelessElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_link_text(wirelessButtonXpath))
        wirelessElement.click()
        
        #Change to the Settings tab in a Microhard
        settingButtonXpath = "//a[@href='/cgi-bin/webif/coova-chilli.sh']"
        settingButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(settingButtonXpath))
        settingButtonEle.click()
        
        #Change Hostname Field
        radiusIDFieldXpath = "coova_chilli_coova_nasid"
        radiusIDFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_name(radiusIDFieldXpath))
        radiusIDFieldElement.clear()
        radiusIDFieldElement.send_keys(radiusID)
        
        #Submit the change, like a commit
        commitFieldXpath = "//a[@href='#'][@id='waitbox']"
        commitFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(commitFieldXpath))
        commitFieldElement.click()


    def checkPage(self):
        print(WebDriverWait(self.driver, 10).until(EC.title_contains("Summary")))

    def checkPing(self, ip):
        response = os.system("ping -W 1 -c 1 " + ip + " > /dev/null 2>&1")
        if response == 0:
            return True
        else:
            return False

    def checkUp(self, ip):
        cnt = 0
        up = True
        while cnt < 5:
            up = self.checkPing(ip)
            if up == False:
                 break
            cnt += 1
        return(up)


class databaser():
    def readFile(self):
       self.book = {}
       with open('FWP.csv') as csvfile:
           reader = csv.DictReader(csvfile)
           for row in reader:
               self.book[row['MAC']] = row



    def getDevice(self, mac):
        m = re.sub(r':','', mac)
        print("MAC Address" + m) 
        dev = self.book[m]
        return dev


class logger():
    def openLog(self):
        self.log = {}

    def addToLog(self, type, item):
        self.log[type] = item

    def writeToLog(self):
        self.log['MAC']



def run():



def main():
    IPs = ["10.254.0.3","10.254.0.19","10.254.0.35","10.254.0.51","10.254.0.67","10.254.0.83","10.254.0.99"]
#"10.254.4.3","10.254.4.19","10.254.4.35","10.254.4.51","10.254.4.67","10.254.4.83","10.254.4.99"]
    
    db = databaser()
    db.readFile()


    
    for ip in IPs:
        print("********  Loading IP : " + ip)

        device = configgerer()
        configURL = 'http://admin:admin@' + ip + '/'
        device.connect(configURL, ip)
        print(configURL)
        print(device.getMac())
        firmware = device.getFirmware()
        print(firmware)
        if firmware != "v1.1.0 build 1086-20150421-new-feature":
            print("FIRMWARE FAIL!!!")
            break

        print("Uploading Config file")
        device.uploadConfig("/support/microhard/microhard_provision/FWConfig.config")
        print("File Uploaded. Sleep for 2 mins.")
        time.sleep(120)
        print("Sleep for another 2 mins.")
        time.sleep(120)

        device.disconnect()




        device2 = configgerer()
        configURL = 'http://admin:!Cm@fW5102@' + ip + ':8081/'
        device2.connect(configURL, ip)

        print("Checking MAC")
        MAC = device2.getMac()
        print("Device MAC : " + MAC)
        print("Loading settings for device")
        devinfo = db.getDevice(MAC)


        print("********* Setting settings")

                # Hostname & Description
        print("Settings Hostname to : " + devinfo["HOSTNAME"])
        print("Setting Desc to : " + devinfo["DESCRIPTION"])
        device2.setHostname(devinfo["HOSTNAME"], devinfo["DESCRIPTION"])
        print("Hostname SET")

        time.sleep(30)
        print("Desc SET")

                # SSID
        print("Settings SSID to : " + devinfo["SSID"])
        device2.setSSID(devinfo["SSID"])
        time.sleep(80)
        print("SSID SET")

                # NASID
        print("Setting NASID to : " + devinfo["NASID"])
        device2.setRadiusID(devinfo["NASID"])
        print("NASID SET")
        time.sleep(60)

        device2.disconnect()
        print("------------------------------------------------------------------------------")



if __name__=='__main__':main()

