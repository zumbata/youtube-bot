import time
import random
import csv
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
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
    global sleep, site, uas
    for prx in proxies:
        PROXY = prx['ip'] + ':' + prx['port']
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': PROXY,
            'ftpProxy': PROXY,
            'sslProxy': PROXY,
            'noProxy': '',
        })
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities['proxy'] = {
            'proxyType': 'MANUAL',
            'httpProxy': PROXY,
            'ftpProxy': PROXY,
            'sslProxy': PROXY,
            }
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override',
                               random.choice(uas))
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.http', prx['ip'])
        profile.set_preference('network.proxy.http_port', prx['port'])
        profile.set_preference('network.proxy.ssl', prx['ip'])
        profile.set_preference('network.proxy.ssl_port', prx['port'])
        profile.update_preferences()
        try:
            driver = webdriver.Firefox(firefox_profile=profile,proxy=proxy,capabilities=firefox_capabilities)
        except:
            continue
        driver.set_page_load_timeout(20)
        driver.get(site)
        time.sleep(5)
        play = driver.find_element(By.CSS_SELECTOR, '.ytp-play-button')
        text = play.get_attribute('title')
        if (text.find('Play') != -1):
            play.click()
        time.sleep(sleep)
        driver.quit()
        print(f"Viewed the video with proxy {PROXY} successfully!")

uas = LoadUserAgents('ua.txt')
print('Please enter link to search: ')  
site = input()
# site = "https://www.youtube.com/watch?v=4beKpdNqThw"
print('Please enter watchtime') 
sleep = int(input())
# sleep = 30
print('Please enter number of threads') 
num_threads = int(input())
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
