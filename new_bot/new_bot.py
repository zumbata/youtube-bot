from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from datetime import datetime
import random, json, base64, sys

def LoadUserAgents(uafile):
	uas = []
	with open(uafile, 'r') as uaf:
		for ua in uaf.readlines():
			uas.append(ua.strip())
	return uas

uas = LoadUserAgents('ua.txt')

data = json.loads(base64.b64decode(sys.argv[1]))
site = data['video']
sleep_min = data['min_time']
sleep_max = data['max_time']
# num_threads = data['threads']
proxies = data['proxies']
sleep(data['sleep'])

for proxy in proxies:
	capa = DesiredCapabilities.CHROME
	capa["pageLoadStrategy"] = "none"
	chrome_options = ChromeOptions()
	chrome_options.add_argument('--proxy-server=socks5://' + proxy)
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument(f'user-agent={random.choice(uas)}')
	chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
	chrome_options.add_experimental_option("useAutomationExtension", False)
	driver = webdriver.Chrome(desired_capabilities=capa, options=chrome_options)
	driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
		"source": """
			Object.defineProperty(navigator, 'webdriver', {
				get: () => undefined
			})
		"""
	})
	driver.implicitly_wait(20)
	driver.get(site)
	sleep(5)
	try:
		driver.find_element(By.CSS_SELECTOR, 'div#container.ytd-masthead')
	except:
		print("Bad proxy. Skipping")
		driver.quit()
		continue
	driver.find_element(By.CSS_SELECTOR, 'body').send_keys('k')
	sleep(random.uniform(sleep_min, sleep_max))
	try:
		element = driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', element)
		sleep(random.uniform(5, 10))
		element = driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', element)
		sleep(random.uniform(5, 10))
	except Exception as e:
		print(str(e))
		pass
	print(f"{datetime.now().strftime('%H:%M:%S')} : Viewed the video with proxy {proxy} successfully!")
	driver.quit()