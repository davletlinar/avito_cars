import time


def sleep_time(secs=20) -> None:
    '''sleep for random time with seconds status bar'''
    # secs = random.randint(30, 60)
    for _ in range(secs):
        time.sleep(1)
        print('-', end='', flush=True)
    print(f' {secs}', end='', flush=True)
    print('\n', end='')