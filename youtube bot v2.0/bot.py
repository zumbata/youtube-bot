import time
import random
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pynput.keyboard import Key, Controller
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
    global sleep, site, uas, keyboard
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
        driver = webdriver.Firefox(firefox_profile=profile,
                                   proxy=proxy,
                                   capabilities=firefox_capabilities)
        driver.set_page_load_timeout(80)
        driver.get(site)
        time.sleep(5)
        keyboard.type(prx['username'])
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        keyboard.type(prx['password'])
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(10)
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        time.sleep(sleep)
        driver.quit()
        print(f"Viewed the video with proxy {PROXY} successfully!")

uas = LoadUserAgents('ua.txt')
keyboard = Controller()
print('Please enter link to search: ')  
site = input()
print('Please enter watchtime') 
sleep = int(input())
print('Please enter number of threads') 
num_threads = int(input())
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
