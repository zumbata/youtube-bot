import zipfile
import csv
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from random import uniform
from random import choice
from datetime import datetime
from pyvirtualdisplay import Display

def divide_chunks(l, n):
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def wait(x, y):
	sleep(uniform(x, y))

def find_element(waitt, by, strr):
	return waitt.until(EC.visibility_of_element_located((by, strr)))

def mydriver(ip, port, username, password):
	manifest_json = """
	{
		"version": "1.0.0",
		"manifest_version": 2,
		"name": "Chrome Proxy",
		"permissions": [
			"proxy",
			"tabs",
			"unlimitedStorage",
			"storage",
			"<all_urls>",
			"webRequest",
			"webRequestBlocking"
		],
		"background": {
			"scripts": ["background.js"]
		},
		"minimum_chrome_version":"22.0.0"
	}
	"""

	background_js = """
	var config = {
			mode: "fixed_servers",
			rules: {
			singleProxy: {
				scheme: "http",
				host: "%s",
				port: parseInt(%s)
			},
			bypassList: ["localhost"]
			}
		};

	chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

	function callbackFn(details) {
		return {
			authCredentials: {
				username: "%s",
				password: "%s"
			}
		};
	}

	chrome.webRequest.onAuthRequired.addListener(
				callbackFn,
				{urls: ["<all_urls>"]},
				['blocking']
	);
	""" % (ip, port, username, password)
	capa = DesiredCapabilities.CHROME
	capa["pageLoadStrategy"] = "none"
	userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
	chrome_options = ChromeOptions()
	pluginfile = 'proxy_auth_plugin.zip'
	with zipfile.ZipFile(pluginfile, 'w') as zp:
		zp.writestr("manifest.json", manifest_json)
		zp.writestr("background.js", background_js)
	chrome_options.add_extension(pluginfile)
	chrome_options.add_extension('cmedhionkhpnakcndndgjdbohmhepckk.crx')
	chrome_options.add_argument(f'user-agent={userAgent}')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument("--start-maximized")
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
	chrome_options.add_experimental_option("useAutomationExtension", False)
	try:
		driver = webdriver.Chrome(desired_capabilities=capa, chrome_options=chrome_options)
	except:
		sleep(5)
		driver = webdriver.Chrome(desired_capabilities=capa, chrome_options=chrome_options)
	return driver

def func(proxies):
	for proxy in proxies:
		driver = mydriver(proxy['ip'], proxy['port'], proxy['username'], proxy['password'])
		waitt = WebDriverWait(driver, 40)
		main(driver, waitt)

def main(driver, waitt):
	global wanted_link, wanted_time_min, wanted_time_max
	keywords = []
	with open('keywords.csv', encoding='utf-8') as file:
		keywords = file.readlines()
	driver.get('https://www.youtube.com/')
	try:
		find_element(waitt, By.CSS_SELECTOR, 'input#search').send_keys(choice(keywords))
		wait(0.5, 1.5)
		find_element(waitt, By.CSS_SELECTOR, 'input#search').send_keys(Keys.RETURN)
	except:
		return
	for x in range(1,100):
		wait(1.0, 2.5)
		try:
			link = find_element(waitt, By.CSS_SELECTOR, 'ytd-video-renderer.ytd-item-section-renderer:nth-child({}) > div:nth-child(1) > ytd-thumbnail:nth-child(1) > a'.format(str(x)))
		except:
			continue
		driver.execute_script('arguments[0].scrollIntoView();', link)
		href = link.get_attribute('href')
		if href in wanted_link :
			wait(0.5, 1.5)
			driver.execute_script('arguments[0].click();', link)
			break
	wait(wanted_time_min, wanted_time_max)
	try:
		elem = find_element(waitt, By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', elem)
		wait(60, 90)
	except:
		pass
	driver.quit()
	sleep(3)

print("Please enter link to search: ")
wanted_link = input()
print("Please enter min watchtime")
wanted_time_min = int(input())
print("Please enter max watchtime")
wanted_time_max = int(input())
print("Please enter number of threads")
num_threads = int(input())

# wanted_time_min = 60
# wanted_time_max = 90
# wanted_link = 'https://www.youtube.com/watch?v=pRKqlw0DaDI'
# num_threads = 1

all_proxies = []
display = Display(visible=0, size=(800, 600))
display.start()

with open('proxies.csv') as file:
	reader = csv.reader(file, delimiter=';')
	for proxy in reader:
		all_proxies.append({'ip' : proxy[0], 'port' : proxy[1], 'username' : proxy[2], 'password' : proxy[3]})

devided_proxies = list(divide_chunks(all_proxies, int(len(all_proxies)/num_threads)))

for group_proxies in devided_proxies:
	some_thread = threading.Thread(target=func, args=(group_proxies,))
	some_thread.start()

while threading.active_count() > 1:
	sleep(1)

display.stop()