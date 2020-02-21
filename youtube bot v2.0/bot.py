from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import uniform
from random import choice
from datetime import datetime

def wait(x, y):
	sleep(uniform(x, y))

def find_element(by, strr):
	global waitt
	return waitt.until(EC.visibility_of_element_located((by, strr)))
	
def mydriver():
	options = Options()
	options.headless = False
	return webdriver.Firefox(options=options)

def main():
	global driver, waitt
	keywords = []
	# wanted_link = input()
	wanted_link = 'https://www.youtube.com/watch?v=pRKqlw0DaDI'
	with open('keywords.csv') as file:
		keywords = file.readlines()
	driver.get('https://www.youtube.com/')
	search_bar = find_element(By.CSS_SELECTOR, 'input#search')
	search_bar.send_keys(choice(keywords))
	wait(0.5, 1.5)
	search_bar.send_keys(Keys.RETURN)
	for x in range(1,50):
		wait(1.0, 2.5)
		link = find_element(By.CSS_SELECTOR, 'ytd-video-renderer.ytd-item-section-renderer:nth-child({}) > div:nth-child(1) > ytd-thumbnail:nth-child(1) > a'.format(str(x)))
		driver.execute_script('arguments[0].scrollIntoView();', link)
		href = link.get_attribute('href')
		if href in wanted_link :
			wait(0.5, 1.5)
			driver.execute_script('arguments[0].click();', link)
			break
	time_dur = find_element(By.CSS_SELECTOR, '.ytp-time-duration').text
	if len(time_dur.split(':')) == 2: 
		time_dur = '00:' + time_dur
	pt = datetime.strptime(time_dur,'%H:%M:%S')
	total_seconds = pt.second + pt.minute*60 + pt.hour * 3600
	wait(total_seconds * 0.5, total_seconds * 0.6)
	elem = find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
	driver.execute_script('arguments[0].click();', elem)
	time_dur = find_element(By.CSS_SELECTOR, '.ytp-time-duration').text
	if len(time_dur.split(':')) == 2: 
		time_dur = '00:' + time_dur
	pt = datetime.strptime(time_dur,'%H:%M:%S')
	total_seconds = pt.second + pt.minute*60 + pt.hour * 3600
	wait(total_seconds * 0.05, total_seconds * 0.1)
	driver.quit()

driver = mydriver()
waitt = WebDriverWait(driver, 30)
main()
