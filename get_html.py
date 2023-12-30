from typing import IO
from icecream import ic
import json
import ssl
import random

from urllib.request import urlopen, Request, ProxyHandler, build_opener
from urllib.error import HTTPError, URLError
import sys

def make_headers(headers_file: IO, user_agent_file: IO) -> dict:
    with open(user_agent_file) as f:
        user_agents_lst = f.read().splitlines()
    with open(headers_file) as f:
        headers = json.load(f)
        headers['User-Agent'] = random.choice(user_agents_lst)
    return headers

def get_html(url) -> str:
    
    switch = 0 # 0 - no proxy, 1 - proxy
    
    # proxy settings
    proxy_ip = '109.195.6.217'
    proxy_port = '40426'
    proxy_username = 'fb6b6d6a56'
    proxy_pswrd = '5bba16d6b6'
    
    proxies = {'http': f'http://{proxy_username}:{proxy_pswrd}@{proxy_ip}:{proxy_port}',
                'https': f'http://{proxy_username}:{proxy_pswrd}@{proxy_ip}:{proxy_port}'}

    # Create a custom SSL context with verification disabled
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    if switch == 1:
        http = Request(url, headers=make_headers('headers.json', 'user-agent.txt'))
        proxy_support = ProxyHandler(proxies)
        opener = build_opener(proxy_support)
        
        response = opener.open(http, context=ssl_context)
        return response.read()
            
    else:
        # configure request attributes
        http = Request(url, headers=make_headers('headers.json', 'user-agent.txt'))
        
        response = urlopen(http, context=ssl_context)
        return response.read()