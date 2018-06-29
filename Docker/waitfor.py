#!/usr/bin/env python3

import os
import re
import time
import socket
import threading


REDIS_URL_PORT_RE = re.compile(r'^(?:.*://)?((?:\d+.){3}\d+)(?::(\d+))?$')


def __wait(addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((addr, port))
            s.close()
            return
        except socket.error:
            time.sleep(0.1)


def wait_redis():
    hostname = os.environ.get('REDIS_URL')
    if hostname is None:
        addr, port = 'redis', 6379
    else:
        match = REDIS_URL_PORT_RE.match(hostname)
        if not match:
            raise ValueError("redis url doesn't match ip:port pattern")
        addr, port = match.groups()
        port = int(port)
    print('waiting for redis')
    __wait(addr, port)
    print('redis ready')


def main(waits):
    threads = [threading.Thread(target=waiter) for waiter in waits]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    import sys

    map_ = {
        'redis': wait_redis,
    }
    
    if len(sys.argv) == 1:
        sys.exit(1)
    elif len(sys.argv) == 2:
        map_[sys.argv[1]]()
    else:
        waits = [map_[key] for key in sys.argv[1:]]
        main(waits)
