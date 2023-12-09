

import random
import time


def sleep_time(secs: int) -> None:
    """sleep for random time with countdown"""
    for _ in range(secs):
        time.sleep(1)
        print('-', end='', flush=True)
    print(f' {secs}', end='', flush=True)
    print('\n', end='')
        
sleep_time(random.randint(12, 16))