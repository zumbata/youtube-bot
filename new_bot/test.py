from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

proxy = '45.77.91.16:42347 '
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
chrome_options = ChromeOptions()
chrome_options.add_argument('--proxy-server=socks5://' + proxy)
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
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
for i in range(20):
    driver.get('https://www.youtube.com/watch?v=MxFoEVzxxb8')
    sleep(5)
    print(driver.page_source)
    play = driver.find_element(By.CSS_SELECTOR, 'body').send_keys('k')
    sleep(30)
    driver.quit()
