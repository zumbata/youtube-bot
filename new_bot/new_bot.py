from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime
import random, json, base64, sys, os

data = json.loads(base64.b64decode(sys.argv[1]))

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
chrome_options = ChromeOptions()
chrome_options.add_argument('--proxy-server=socks5://' + data['proxy'])
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(f'user-agent={data["user_agent"]}')
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

while True:
	video = random.choice(data['videos'])
	driver.get(video['href'])
	try:
		WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "movie_player")))
	except:
		continue
	sleep(5)
	driver.find_element(By.CSS_SELECTOR, 'body').send_keys('k')
	sleep(random.uniform(video['min_time'], video['max_time']))
	try:
		element = driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', element)
		sleep(random.uniform(5, 10))
		element = driver.find_element(By.CSS_SELECTOR, 'ytd-compact-video-renderer.style-scope:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)')
		driver.execute_script('arguments[0].click();', element)
		sleep(random.uniform(5, 10))
	except Exception as e:
		pass