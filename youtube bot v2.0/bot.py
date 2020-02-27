import time
import random
import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
import threading

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
    global sleep_min, sleep_max, site, uas
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
print('Please enter link to search: ')  
site = input()
print('Please enter min watchtime') 
sleep_min = int(input())
print('Please enter max watchtime') 
sleep_max = int(input())
print('Please enter number of threads') 
num_threads = int(input())
# site = "https://www.youtube.com/watch?v=4beKpdNqThw"
# sleep_min = 20
# sleep_max = 25
# num_threads = 1

all_proxies = []
with open('proxies.csv') as file:
    reader = csv.reader(file, delimiter=';')
    for proxy in reader:
        all_proxies.append({
            'ip': proxy[0],
            'port': proxy[1],
            'username': proxy[2],
            'password': proxy[3],
            })
devided_proxies = list(divide_chunks(all_proxies, int(len(all_proxies)
                       / num_threads)))
for group_proxies in devided_proxies:
    some_thread = threading.Thread(target=func, args=(group_proxies, ))
    some_thread.start()
while threading.active_count() > 1:
    time.sleep(1)
