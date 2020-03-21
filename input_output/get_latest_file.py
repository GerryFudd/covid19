from selenium import webdriver
from time import sleep
from shutil import move
from os import environ

DOWNLOADED_FILE_NAME_PATTERN = 'total-cases-covid-19'

def get_latest_file(new_file_name):
  driver = webdriver.Chrome()
  driver.get('https://ourworldindata.org/grapher/total-cases-covid-19-who')
  data_tab_element = driver.find_element_by_xpath("//a[@data-track-note='chart-click-data']")
  data_tab_element.click()
  download_element = driver.find_element_by_xpath(f"//a[contains(@download, '{DOWNLOADED_FILE_NAME_PATTERN}')]")
  downloaded_file_name = download_element.get_attribute('download')
  download_element.click()
  sleep(1)
  driver.close()

  move(f'{environ["HOME"]}/Downloads/{downloaded_file_name}', new_file_name)
