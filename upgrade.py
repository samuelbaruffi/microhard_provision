from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


class upgrader():
    def connect(self, site):
        p = webdriver.FirefoxProfile()
        p.set_preference('webdriver.log.file','/tmp/firefox_console')
        self.driver = webdriver.Firefox(p)
        self.driver.get(site)

    def upgradeFirmware(self, firmware="/support/microhard/microhard_provision/firmware.bin"):
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
        
        element = WebDriverWait(driver, 600).until(EC.title_contains("Summary"))

        #sleep for 10 minutes while upgrade
        #time.sleep(600)

    def checkFirmware(self):
        driver = self.driver
        maintenanceButtonXpath = ".//*[@id='submenu']/li[5]/a"
        maintenanceButtonEle = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(maintenanceButtonXpath))
        maintenanceButtonEle.click()
        return(self.driver.find_element_by_xpath("//div[@id='content']/div/table[2]/tbody/tr[2]/td[4]").text)

#//*[@id="content"]/div[1]/table[2]/tbody/tr[2]/td[4]


    def tearDown(self):
        self.driver.quit()

    def check_ping(self, hostname):
        response = os.system("ping -c 1 " + hostname + " > /dev/null 2>&1")
        if response == 0:
            return True
        else:
            return False


def main():
    IPs = ["10.254.0.3","10.254.0.19","10.254.0.35","10.254.0.51","10.254.0.67","10.254.0.83","10.254.0.99"] 
    
    for ip in IPs: 
        cnt = 0
        while cnt < 5:
            check = check_ping(ip)
            cnt += 1

        
        
        configURL = 'http://admin:admin@' + ip + '/'
        device = upgrader()
        #print(check_ping(ip))
        device.connect(configURL)
        print(device.checkFirmware())
        device.tearDown()

if __name__=='__main__':main()

