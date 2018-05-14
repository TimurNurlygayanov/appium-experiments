# To successfully run this test you should have connected android device
# This script will just open AliExpress Android app on your android device
# AliExpress app should be already installed.
 
from appium import webdriver


desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '8.0'
desired_caps['deviceName'] = 'Android'

desired_caps['appPackage'] = 'com.alibaba.aliexpresshd'
desired_caps['appActivity'] = 'com.aliexpress.module.home.MainActivity'


driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

