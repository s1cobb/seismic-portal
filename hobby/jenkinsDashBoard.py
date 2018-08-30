import os
import re
import sys
import time
import loginPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ConfigPage:
   ''' This class will setup the configuration for a simple
       freestyle project in jenkins
   '''

   def __init__(self, browser):
       self.drv = browser

   def set_project_name(self,desc='default message'):
       drv = self.drv
       link_elem = drv.find_element_by_link_text('New Item')
       link_elem.click()
       time.sleep(2)
       desc = drv.find_element_by_name('name')
       desc.send_keys('testproject')
       time.sleep(2)

       style = drv.find_element_by_class_name('hudson_model_FreeStyleProject')
       style.click()
       time.sleep(2)
       ok_butt = drv.find_element_by_id('ok-button')
       ok_butt.click()

   def set_chkbox(self, chkbox_name=None ):
       drv = self.drv
       wait = WebDriverWait(drv, 10)
       chk_elem = wait.until(EC.presence_of_element_located((By.ID, chkbox_name)))
       chk_elem.click()

   def set_radio_but(self, radiobut=None):
       drv = self.drv
       wait = WebDriverWait(drv, 10)
       chk_elem = wait.until(EC.presence_of_element_located((By.ID,'radio-block-1')))
       chk_elem.click()
   
   def set_test_script_path(self, path=None):
       drv = self.drv
       elm = drv.find_element_by_name('_.url')
       elm.send_keys(path)

   def set_build_time_field(self):
       drv = self.drv
       elm = drv.find_element_by_xpath(".//*[@id='main-panel']/div/div/div/form/table/tbody/tr[114]/td[3]/textarea")
       elm.send_keys('H/6 * * * *')
   
   def hit_button(self, click_button):
       drv = self.drv
       wait = WebDriverWait(drv, 10)
       chk_elem = wait.until(EC.presence_of_element_located((By.ID,click_button)))
       chk_elem.click()

   def set_description(self):
       drv = self.drv
       wait = WebDriverWait(drv, 10)
       elm = wait.until(EC.presence_of_element_located((By.XPATH, ".//*[@id='main-panel']/div/div/div/form/table/tbody/tr[4]/td[3]/textarea")))
       elm.send_keys('my automated jenkins setup with selenium')
   
   def set_execute_shell(self):
       drv = self.drv
       print("url %s" % drv.current_url)

       wait = WebDriverWait(drv, 10)
       chk_elem = wait.until(EC.presence_of_element_located((By.ID,'yui-gen40')))
       chk_elem.click()

       wait = WebDriverWait(drv, 10)
       elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'CodeMirror')))
       drv.execute_script("return arguments[0].scrollIntoView();", elem)
       time.sleep(2)
       if elem.is_displayed():
          print("elem is visible")

       assert elem.is_displayed()
       elem.send_keys('/data/test1.py')

if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.get('http://54.224.3.74:8080')
    
    login = loginPage.JenkinsLogin(browser)
    login.user_login('steve')
    login.user_password('steve')
    login.click_login('yui-gen1')

    dashbd = ConfigPage(browser)
    dashbd.set_project_name()
    dashbd.set_description()
    dashbd.set_chkbox('cb9')
    dashbd.set_radio_but('radio-block-1')
    dashbd.set_test_script_path('/data')
    time.sleep(5)
    dashbd.set_chkbox('cb19')
    time.sleep(5)
    dashbd.set_build_time_field()
    time.sleep(2)
    dashbd.hit_button('yui-gen19-button')
    time.sleep(2)
    dashbd.set_execute_shell()
    time.sleep(2)
    dashbd.hit_button('yui-gen28-button')
    time.sleep(2)
    dashbd.hit_button('yui-gen37-button')
