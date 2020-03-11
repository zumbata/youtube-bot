import time
import random
import json
import base64
import os
import sys
import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType

# def LoadUserAgents(uafile):
# 	uas = []
# 	with open(uafile, 'r') as uaf:
# 		for ua in uaf.readlines():
# 			uas.append(ua.strip())
# 	random.shuffle(uas) uas

# uas = LoadUserAgents(f'{os.path.dirname(os.path.realpath(__file__))}/ua.txt')

data = json.loads(base64.b64decode(sys.argv[1]))
site = data['video']
sleep_min = data['min_time']
sleep_max = data['max_time']
num_threads = data['threads']
proxies = data['proxies']
keywords = data['keywords']
time.sleep(data['sleep'])

for proxy in proxies:
	options = Options()
	options.headless = True
	options.log.level = "trace"
	profile = webdriver.FirefoxProfile()
	profile.set_preference("network.proxy.type", 1)
	profile.set_preference('network.proxy.socks', proxy.split(':')[0])
	profile.set_preference('network.proxy.socks_port', int(proxy.split(':')[1]))
	# profile.set_preference('general.useragent.override', random.choice(uas))
	profile.update_preferences()
	try:
		driver = webdriver.Firefox(firefox_profile=profile, options=options)
	except Exception as e:
		print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
		print(str(e))
	driver.set_page_load_timeout(20)
	driver.implicitly_wait(20)
	try:
		driver.get('https://youtube.com/')
	except Exception as e:
		print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
		print(str(e))
		driver.close()
	try:
		search = driver.find_element(By.CSS_SELECTOR, 'input#search')
		button = driver.find_element(By.CSS_SELECTOR, '#search-icon-legacy')
		driver.execute_script(f'arguments[0].value = "{random.choice(keywords)}";', search)
		driver.execute_script(f'arguments[0].click();', button)
	except Exception as e:
		print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
		print(str(e))	
		driver.close()
	flag = False
	for x in range(1,20):
		try:
			link = driver.find_element(By.CSS_SELECTOR, 'ytd-video-renderer.ytd-item-section-renderer:nth-child({}) > div:nth-child(1) > ytd-thumbnail:nth-child(1) > a'.format(str(x)))
		except Exception as e:
			print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
			print(str(e))
			continue
		driver.execute_script('arguments[0].scrollIntoView();', link)
		href = link.get_attribute('href')
		if href in site :
			driver.execute_script(f'arguments[0].click();', link)
			flag = True
			break
	if flag == False:
		driver.get(site)
	try:
		play = driver.find_element(By.CSS_SELECTOR, '.ytp-play-button')
	except Exception as e:
		print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
		print(str(e))
		driver.close()
	text = play.get_attribute('title')
	if (text.find('Play') != -1):
		try:
			driver.execute_script('arguments[0].click();', play)
		except Exception as e:
			print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
			print(str(e))
			driver.close()
	try:
		time.sleep(random.uniform(sleep_min, sleep_max))
		element = driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', element)
		time.sleep(random.uniform(5, 10))
		element = driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', element)
		time.sleep(random.uniform(5, 10))
	except Exception as e:
		print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
		print(str(e))
		driver.close()
	print(f"{datetime.now().strftime('%H:%M:%S')} : Viewed the video with proxy {proxy} successfully!")
	driver.close()