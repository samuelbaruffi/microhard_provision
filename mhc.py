from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import re

class configgerer():
    def connect(self, ip):
        self.configURL = 'http://admin:admin@' + ip + '/'
        self.ip = ip
        p = webdriver.FirefoxProfile()
        p.set_preference('webdriver.log.file','/tmp/firefox_console')
        self.driver = webdriver.Firefox(p)
        self.driver.get(self.configURL)

    def tearDown(self):
        self.driver.quit()

    def checkMac(self):
        print(self.driver.find_element_by_xpath("//div[@id='content']/div[3]/table[2]/tbody/tr[3]/td[4]").text)
        
    def checkFirmware(self):
        driver = self.driver
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        return(self.driver.find_element_by_xpath("//div[@id='content']/div/table[2]/tbody/tr[2]/td[4]").text)

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



class database():
    def readFile(self):
       self.book = {}
       with open('FWP.csv') as csvfile:
           reader = csv.DictReader(csvfile)
           for row in reader:
               self.book[row['MAC']] = row



    def getDevice(self, mac):
        print(mac)
        m = re.sub(r':','',mac)
        print(m) 
        print(self.book)
        dev = self.book[m]
        print(dev)       




def main():
    IPs = ["10.254.0.3","10.254.0.19","10.254.0.35","10.254.0.51","10.254.0.67","10.254.0.83","10.254.0.99"] 
    
    db = database()
    db.readFile()
    
    for ip in IPs:
        device = configgerer()
        #device.checkUp(ip)
        device.connect(ip)
        #print(device.checkPing(ip))
        MAC = device.checkMac()
        db.getDevice(MAC)
        device.tearDown()

if __name__=='__main__':main()

