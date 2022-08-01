# std import, not used
import os
import numpy as np
import pandas as pd
# import needed
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    print('start...')
    # download the chrome driver version same as your chrome version
    driver = webdriver.Chrome('./selenium/chromedriver.exe')
    # example link (MY BLOG)
    driver.get("https://www.giomin.com")
    # print the window name
    print(driver.title)
    print('...end')
