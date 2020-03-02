import time
import random
import json
import threading
import base64
import sys
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
		options.headless = True
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
			print(f"Skipped watching video with proxy {PROXY} because of error in the driver")
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
			print(f"Skipped watching video with proxy {PROXY} because of error in the the search")
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
			print(f"Skipped watching video with proxy {PROXY} because of error in the the play button")
			driver.quit()
			continue
		text = play.get_attribute('title')
		if (text.find('Play') != -1):
			try:
				play.click()
			except:
				print(f"Skipped watching video with proxy {PROXY} because of error in the the play button")
				driver.quit()
				continue
		time.sleep(random.uniform(sleep_min, sleep_max))
		driver.quit()
		print(f"Viewed the video with proxy {PROXY} successfully!")

uas = LoadUserAgents('ua.txt')
data = json.loads(base64.b64decode(sys.argv[1]))
site = data['video']
sleep_min = data['min_time']
sleep_max = data['max_time']
num_threads = data['threads']
all_proxies = data['proxies'].split()
keywords = data['keywords'].split()

devided_proxies = list(divide_chunks(all_proxies, int(len(all_proxies)
					   / num_threads)))
for group_proxies in devided_proxies:
	some_thread = threading.Thread(target=func, args=(group_proxies, ))
	some_thread.start()