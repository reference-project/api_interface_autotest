# coding=utf-8

from selenium import webdriver
from time import sleep

b = webdriver.Firefox()
for i in range(0, 1000):
    b.get('https://sdk.trusfort.com/zentaopms/www/index.php?m=user&f=login')
    b.find_element_by_id('account').send_keys('huangshuai')
    b.find_element_by_xpath('/html/body/div/div[1]/div[2]/form/table/tbody/tr[2]/td/input').send_keys('Xd170213')
    b.find_element_by_id('submit').click()
    sleep(1)
    b.find_element_by_xpath('/html/body/header/div/div/a[1]').click()
