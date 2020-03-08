import time
import random
import json
import math
import threading
import base64
import os
import sys
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType

def LoadUserAgents(uafile):
	uas = []
	with open(uafile, 'r') as uaf:
		for ua in uaf.readlines():
			uas.append(ua.strip())
	random.shuffle(uas)
	return uas

def divide_chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]

def func(proxies):
	global sleep_min, sleep_max, site, keywords#, uas
	for prx in proxies:
		PROXY = prx['ip'] + ':' + prx['port']
		options = Options()
		options.headless = True
		proxy = Proxy({
			'proxyType': ProxyType.MANUAL,
			'httpProxy': PROXY,
			'ftpProxy': PROXY,
			'sslProxy': PROXY,
			'noProxy': ''
		})
		# firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
		# firefox_capabilities['marionette'] = True
		# firefox_capabilities['proxy'] = {
		# 	'proxyType': 'MANUAL',
		# 	'httpProxy': PROXY,
		# 	'ftpProxy': PROXY,
		# 	'sslProxy': PROXY,
		# }
		# profile = webdriver.FirefoxProfile()
		# profile.set_preference('general.useragent.override', random.choice(uas))
		try:
			driver = webdriver.Firefox(options=options, proxy=proxy)
		except Exception as e:
			print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
			print(str(e))
			continue
		driver.set_page_load_timeout(10)
		driver.implicitly_wait(10)
		try:
			driver.get('https://youtube.com/')
		except Exception as e:
			print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
			print(str(e))
			driver.quit()
			continue
		try:
			search = driver.find_element(By.CSS_SELECTOR, 'input#search')
			button = driver.find_element(By.CSS_SELECTOR, '#search-icon-legacy')
			driver.execute_script(f'arguments[0].value = "{random.choice(keywords)}";', search)
			driver.execute_script(f'arguments[0].click();', button)
		except Exception as e:
			print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
			print(str(e))
			driver.quit()
			continue
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
			driver.quit()
			continue
		text = play.get_attribute('title')
		if (text.find('Play') != -1):
			try:
				driver.execute_script('arguments[0].click();', play)
			except Exception as e:
				print(f"{datetime.now().strftime('%H:%M:%S')} : Exception occured in line {sys._getframe().f_lineno}")
				print(str(e))
				driver.quit()
				continue
		time.sleep(random.uniform(sleep_min, sleep_max))
		element = driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', element)
		time.sleep(random.uniform(5, 10))
		element = driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', element)
		time.sleep(random.uniform(5, 10))
		print(f"{datetime.now().strftime('%H:%M:%S')} : Viewed the video with proxy {PROXY} successfully!")
		driver.quit()

# uas = LoadUserAgents(f'{os.path.dirname(os.path.realpath(__file__))}/ua.txt')
data = json.loads(base64.b64decode(sys.argv[1]))
# data = {
# 	'video' : 'https://www.youtube.com/watch?v=pRKqlw0DaDI',
# 	'min_time' : '60',
# 	'max_time' : '70',
# 	'threads' : '2',
# 	'proxies' : '168.235.71.27:12907\n168.235.71.27:12906\n168.235.71.27:12905\n168.235.71.27:12904\n168.235.71.27:12903',
# 	'keywords' : 'hello world\nhello world\nhello world\nhello world\n'
# }
site = data['video']
sleep_min = int(data['min_time'])
sleep_max = int(data['max_time'])
num_threads = int(data['threads'])
all_proxies = []
proxies = data['proxies'].split()
for proxy in proxies:
	proxy_splited = proxy.split(':')
	all_proxies.append({'ip' : proxy_splited[0], 'port' : proxy_splited[1]})
keywords = [x.strip('\t').strip('\n').strip() for x in data['keywords'].split('\n')]

devided_proxies = list(divide_chunks(all_proxies, math.floor(len(all_proxies) / num_threads)))
for group_proxies in devided_proxies:
	some_thread = threading.Thread(target=func, args=(group_proxies, ))
	some_thread.start()
	time.sleep(2)