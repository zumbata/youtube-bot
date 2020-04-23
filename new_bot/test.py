from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

# proxy = '209.250.237.162:35584'
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
chrome_options = ChromeOptions()
# chrome_options.add_argument('--proxy-server=socks5://' + proxy)
chrome_options.add_argument("--headless")
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
driver.implicitly_wait(100)

driver.get('https://www.youtube.com/watch?v=MxFoEVzxxb8')

sleep(30)

driver.quit()