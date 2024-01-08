from typing import IO
from icecream import ic
import json
import random
from sleep_time import sleep_time
from flask import Flask

def make_headers(headers_file: IO, user_agent_file: IO) -> dict:
    with open(user_agent_file) as f:
        user_agents_lst = f.read().splitlines()
    with open(headers_file) as f:
        headers = json.load(f)
        headers['User-Agent'] = random.choice(user_agents_lst)
    return headers

def get_html(url) -> str:
    headers = make_headers('headers.json', 'user-agent.txt')
    try:
        
    except Exception as e:
        print(f"❌ {e}")
        sleep_time()
    return html.text

url = 'https://www.avito.ru/all/avtomobili/volkswagen/passat?p=14'
print(get_html(url))

# import Flask and make an http request
