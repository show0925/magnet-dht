#! usr/bin/python
# encoding=utf-8


from threading import Thread
from magnet_dht.crawler import *
from magnet_dht.magnet_to_torrent_aria2c import *


# 服务 host
SERVER_HOST = "0.0.0.0"
# 服务端口
SERVER_PORT = 9090
# 是否使用全部进程
MAX_PROCESSES = 2 // 2 or cpu_count()


def _start_thread(offset, parse):
    """
    启动线程

    :param offset: 端口偏移值
    """
    dht = DHTServer(SERVER_HOST, SERVER_PORT + offset, offset)
    threads = [
        Thread(target=dht.send_find_node_forever),
        Thread(target=dht.receive_response_forever),
        Thread(target=dht.bs_timer),
    ]
    if parse:
        threads.append(Thread(target=magnet2torrent))        

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def start_server(parse=False):
    """
    多线程启动服务
    """
    processes = []
    for i in range(MAX_PROCESSES):
        processes.append(Process(target=_start_thread, args=(i,parse)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

