#!/usr/bin/python

import os
import re
import time
import unittest
import loginPage
from selenium import webdriver

class Login(unittest.TestCase):
   
    def setUp(self):
       self.driver = webdriver.Firefox()

    @classmethod
    def setUpClass(self):
       self.ip_addr = 'http://54.224.3.74:8080'

    # test number 1
    def test_valid_usr_pw(self):
       self.driver.get(self.ip_addr)
       login = loginPage.JenkinsLogin(self.driver)
       login.user_login('steve')
       login.user_password('steve')
       login.click_login('yui-gen1')
       self.assertEqual(self.driver.title,'Dashboard [Jenkins]')
       login.exit_jenkins()
       login.close_browser()

    # test number 2 
    def test_invalid_user(self):
       self.driver.get(self.ip_addr)
       login = loginPage.JenkinsLogin(self.driver)
       login.user_login('bob')
       login.user_password('steve')
       login.click_login('yui-gen1') 
       self.assertEqual(self.driver.title,'Login Error [Jenkins]')
       login.click_retry('Try again')
       self.assertEqual(self.driver.title, 'Jenkins')

       login.user_login('steve')
       login.user_password('steve')
       self.assertEqual(self.driver.title,'Jenkins')
       login.click_login('yui-gen1')
       login.exit_jenkins()
       login.close_browser()

    # test number 3 
    def test_invalid_passwd(self):
       self.driver.get(self.ip_addr)
       login = loginPage.JenkinsLogin(self.driver)
       login.user_login('steve')
       login.user_password('jkjk')
       login.click_login('yui-gen1')
       self.assertEqual(self.driver.title,'Login Error [Jenkins]')
       login.close_browser()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass


if __name__ == '__main__':
   unittest.main()
