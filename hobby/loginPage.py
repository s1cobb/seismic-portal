#!/usr/bin/python

import os
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class JenkinsLogin:
   def __init__(self, browser=None):
       self.dr = browser 

   def user_login(self, userlogin=None):
       dr = self.dr
       wait = WebDriverWait(dr,10)
       elem = wait.until(EC.presence_of_element_located((By.NAME, 'j_username')))
       elem.send_keys(userlogin)

   def user_password(self, passwd):
       dr = self.dr
       wait = WebDriverWait(dr,10)
       pw = wait.until(EC.presence_of_element_located((By.NAME,'j_password')))
       pw.send_keys(passwd)


   def clear_text(self):
       dr = self.dr
       wait = WebDriverWait(dr,10)
       elem = wait.until(EC.presence_of_element_located((By.NAME, 'j_username')))
       elem.clear()

       dr = self.dr
       wait = WebDriverWait(dr,10)
       pw = wait.until(EC.presence_of_element_located((By.NAME,'j_password')))
       pw.clear()

   def click_retry(self, link_value=None):
       dr = self.dr
       wait = WebDriverWait(dr,10)
       pw = wait.until(EC.presence_of_element_located((By.LINK_TEXT,link_value)))
       pw.click()

   def click_login(self, login_id=None):
       dr = self.dr
       wait = WebDriverWait(dr,10)
       login_but = wait.until(EC.presence_of_element_located((By.ID,login_id)))
       login_but.click()

   def exit_jenkins(self):
       dr = self.dr
       nav = dr.find_element_by_link_text('log out') 
       nav.click()

   def close_browser(self):
       self.dr.close()

 
if __name__ == '__main__':
   browser = webdriver.Firefox()
   browser.get('http://54.165.85.62:8080')

   login = JenkinsLogin(browser)
   login.user_login('steve')
   time.sleep(2)
   login.user_password('steve')
   time.sleep(2)
   login.click_login()
   time.sleep(2)
   login.exit_jenkins()
   time.sleep(2)
   login.close_browser() 
        
