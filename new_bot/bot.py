import time
import random
import json
import threading
import base64
import os
import sys
import subprocess
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

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
	global sleep_min, sleep_max, site, uas, keywords
	for prx in proxies:
		PROXY = prx['ip'] + ':' + prx['port']
		options = Options()
		# options.headless = True
		firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
		firefox_capabilities['marionette'] = True
		firefox_capabilities['proxy'] = {
			'proxyType': 'MANUAL',
			'httpProxy': PROXY,
			'ftpProxy': PROXY,
			'sslProxy': PROXY,
		}
		profile = webdriver.FirefoxProfile()
		profile.set_preference('general.useragent.override', random.choice(uas))
		try:
			driver = webdriver.Firefox(firefox_profile=profile, options=options, capabilities=firefox_capabilities)
		except:
			try:
				driver.quit()
			except:
				pass
			continue
		driver.set_page_load_timeout(20)
		driver.implicitly_wait(20)
		driver.get('https://youtube.com/')
		try:
			driver.find_element(By.CSS_SELECTOR, 'input#search').send_keys(random.choice(keywords))
			driver.find_element(By.CSS_SELECTOR, 'input#search').send_keys(Keys.RETURN)
		except:
			driver.quit()
			continue
		flag = False
		for x in range(1,20):
			try:
				link = driver.find_element(By.CSS_SELECTOR, 'ytd-video-renderer.ytd-item-section-renderer:nth-child({}) > div:nth-child(1) > ytd-thumbnail:nth-child(1) > a'.format(str(x)))
			except:
				continue
			driver.execute_script('arguments[0].scrollIntoView();', link)
			href = link.get_attribute('href')
			if href in site :
				link.click()
				flag = True
				break
		if flag == False:
			driver.get(site)
		try:
			play = driver.find_element(By.CSS_SELECTOR, '.ytp-play-button')
		except:
			driver.quit()
			continue
		text = play.get_attribute('title')
		if (text.find('Play') != -1):
			try:
				play.click()
			except:
				driver.quit()
				continue
		time.sleep(random.uniform(sleep_min, sleep_max))
		driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)').click()
		time.sleep(random.uniform(10, 20))
		driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)').click()
		time.sleep(random.uniform(5, 10))
		driver.quit()

uas = LoadUserAgents(f'{os.path.dirname(os.path.realpath(__file__))}/ua.txt')
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
keywords = data['keywords'].split('\n')

devided_proxies = list(divide_chunks(all_proxies, int(len(all_proxies) / num_threads)))
for group_proxies in devided_proxies:
	some_thread = threading.Thread(target=func, args=(group_proxies, ))
	some_thread.start()