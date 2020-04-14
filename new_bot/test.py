from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys


options = Options()
options.headless = True
options.log.level = "trace"
prox = sys.argv[1]
# prox = '209.250.237.162:33361'
ip = prox.split(':')[0]
port = prox.split(':')[1]
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", ip)
profile.set_preference("network.proxy.socks_port", int(port))
profile.set_preference("network.proxy.socks_version", 5)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile=profile, options=options)
driver.get("https://whatismyipaddress.com/")
print(driver.find_element_by_css_selector('#ipv6').text)
driver.quit()