from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
prox = sys.argv[1]
ip = prox.split(':')[0]
port = prox.split(':')[1]
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", ip)
profile.set_preference("network.proxy.socks_port", int(port))
profile.set_preference("network.proxy.socks_version", 5)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile=profile)

driver.get("https://ipecho.net/plain")
print(driver.page_source)
driver.quit()