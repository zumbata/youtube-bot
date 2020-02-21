import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from random import uniform
from random import choice
from datetime import datetime
from fake_useragent import UserAgent

def wait(x, y):
	sleep(uniform(x, y))

def find_element(by, strr):
	global waitt
	elem = waitt.until(EC.presence_of_element_located((by, strr)))
	driver.execute_script('arguments[0].scrollIntoView();', elem)
	return elem
	
def mydriver():
	capa = DesiredCapabilities.CHROME
	capa["pageLoadStrategy"] = "none"
	userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
	chrome_options = ChromeOptions()
	chrome_options.add_argument(f'user-agent={userAgent}')
	# chrome_options.add_argument("--headless")
	# chrome_options.add_argument("--profile-directory=Profile 1")
	chrome_options.add_extension('cmedhionkhpnakcndndgjdbohmhepckk.crx')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument("--start-maximized")
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
	chrome_options.add_experimental_option("useAutomationExtension", False)
	driver = webdriver.Chrome(desired_capabilities=capa, chrome_options=chrome_options)
	return driver
	

# def switchIP():
# 	os.system("expressvpn disconnect")
# 	os.system("expressvpn connect smart")

accounts = []
keywords = []
comments = []
# wanted_link = input()
wanted_link = 'https://www.youtube.com/watch?v=pRKqlw0DaDI'

with open('accounts.csv') as file:
	reader = csv.reader(file, delimiter=',', quotechar='"')
	for account in reader:
		accounts.append({'email' : account[0],'password' : account[1], 'recovery' : account[2], 'comment' : account[3]})

with open('keywords.csv') as file:
	keywords = file.readlines()

with open('comments.csv') as file:
	comments = file.readlines()

for account in accounts:
# 	switchIP()
	driver  = mydriver()
	waitt  = WebDriverWait(driver, 15)
	driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
	wait(1.5, 2.5)
	try:
		find_element(By.CSS_SELECTOR, '#openid-buttons > button:nth-child(1)').click()
		wait(4, 5.5)
		find_element(By.CSS_SELECTOR, '#identifierId').send_keys(account['email'])
		find_element(By.CSS_SELECTOR, '#identifierNext').click()
		wait(4, 5.5)
		find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(account['password'])
		find_element(By.CSS_SELECTOR, '#passwordNext').click()
		wait(4, 5.5)
		try:
			find_element(By.CSS_SELECTOR, 'li.JDAKTe:nth-child(1) > div:nth-child(1)').click()
			find_element(By.CSS_SELECTOR, 'input#knowledge-preregistered-email-response').send_keys(account['recovery'])
			find_element(By.CSS_SELECTOR, '.zZhnYe').click()
			wait(4, 5.5)
		except :
			pass
		driver.get('https://youtube.com/')
		wait(3.5, 4.5)
		find_element(By.CSS_SELECTOR, 'input#search').send_keys(choice(keywords))
		find_element(By.CSS_SELECTOR, 'input#search').send_keys(Keys.RETURN)
	except:
		driver.quit()
		print("Problem. Trying again.")
# 		switchIP()
		continue
	for x in range(1,50):
		wait(1, 2.5)
		try:
			link = find_element(By.CSS_SELECTOR, 'ytd-video-renderer.ytd-item-section-renderer:nth-child({}) > div:nth-child(1) > ytd-thumbnail:nth-child(1) > a'.format(str(x)))
		except:
			continue
		driver.execute_script('arguments[0].scrollIntoView();', link)
		href = link.get_attribute('href')
		if href in wanted_link :
			wait(0.5, 1.5)
			link.click()
			break
	time_dur = find_element(By.CSS_SELECTOR, '.ytp-time-duration').text
	if len(time_dur.split(':')) == 2: 
		time_dur = '00:' + time_dur
	splited = time_dur.split(":")
	if len(splited[1]) == 1:
		splited[1] = "0{}".format(splited[1])
		time_dur = ":".join(splited)
	pt = datetime.strptime(time_dur,'%H:%M:%S')
	total_seconds = pt.second + pt.minute*60 + pt.hour * 3600
	wait(total_seconds * 0.5, total_seconds * 0.6)
	if account["comment"] == "1" :
		find_element(By.CSS_SELECTOR, '#placeholder-area').click()
		textarea = find_element(By.CSS_SELECTOR, '#contenteditable-textarea')
		textarea.send_keys(choice(comments))
		wait(1.5, 3.5)
		find_element(By.CSS_SELECTOR, '#submit-button').click()
	if find_element(By.CSS_SELECTOR, 'ytd-subscribe-button-renderer.ytd-video-secondary-info-renderer > paper-button:nth-child(1) > yt-formatted-string:nth-child(1)').text == 'Subscribe' :
		wait(1.5, 3.5)
		find_element(By.CSS_SELECTOR, 'ytd-subscribe-button-renderer.ytd-video-secondary-info-renderer > paper-button:nth-child(1)').click()
	if 'style-text' in find_element(By.CSS_SELECTOR, 'ytd-subscribe-button-renderer.ytd-video-secondary-info-renderer > paper-button:nth-child(1) > yt-formatted-string:nth-child(1)').get_attribute('class').split() :
		wait(1.5, 3.5)
		find_element(By.CSS_SELECTOR, 'ytd-toggle-button-renderer.ytd-menu-renderer:nth-child(1) > a:nth-child(1)').click()
	wait(3, 4.5)
	find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)').click()
	wait(3, 4.5)
	time_dur = find_element(By.CSS_SELECTOR, '.ytp-time-duration').text
	if len(time_dur.split(':')) == 2: 
		time_dur = '00:' + time_dur
	splited = time_dur.split(":")
	if len(splited[1]) == 1:
		splited[1] = "0{}".format(splited[1])
		time_dur = ":".join(splited)
	pt = datetime.strptime(time_dur,'%H:%M:%S')
	total_seconds = pt.second + pt.minute*60 + pt.hour * 3600
	wait(total_seconds * 0.05, total_seconds * 0.1)
	driver.quit()
	print("Done. Proceeding with the nex one.")
