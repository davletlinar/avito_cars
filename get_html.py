from typing import IO
from icecream import ic
import json
import random
from sleep_time import sleep_time

from urllib.request import urlopen, Request, ProxyHandler, build_opener
from urllib.error import HTTPError

def make_headers(headers_file: IO, user_agent_file: IO) -> dict:
    with open(user_agent_file) as f:
        user_agents_lst = f.read().splitlines()
    with open(headers_file) as f:
        headers = json.load(f)
        headers['User-Agent'] = random.choice(user_agents_lst)
    return headers

def get_html(url) -> str:
    
    switch = 0 # 0 - no proxy, 1 - proxy
    success = 0
    
    # proxy settings
    proxy_ip = '86.110.189.118'
    proxy_port = '42539'
    proxy_username = 'fb6b6d6a56'
    proxy_pswrd = '5bba16d6b6'
    
    proxies = {'http': f'http://{proxy_username}:{proxy_pswrd}@{proxy_ip}:{proxy_port}',
                'https': f'http://{proxy_username}:{proxy_pswrd}@{proxy_ip}:{proxy_port}'}

    if switch == 1:
        req = Request(url, headers=make_headers('headers.json', 'user-agent.txt'))
        proxy_support = ProxyHandler(proxies)
        opener = build_opener(proxy_support)
        
        response = opener.open(req)
        return response.read()
            
    else:
        # configure request attributes
        req = Request(url, headers=make_headers('headers.json', 'user-agent.txt'))
        
        while success != 1:
            try:
                response = urlopen(req)
                success = 1
            except HTTPError as e:
                print(f"❌ {e}")
                sleep_time(secs=120)
            except Exception as e:
                print(f"❌ {e}")
                sleep_time()
        
        return response.read()