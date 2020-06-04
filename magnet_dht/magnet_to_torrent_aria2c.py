#!usr/bin/python
# encoding=utf-8

from http.client import HTTPConnection
import json
import os
import time
from .utils import get_logger

from .database import RedisClient

# while 循环休眠时间
SLEEP_TIME_PARSEING = 1e-2
SLEEP_TIME_IDEL = 30

SAVE_PATH = ".\\torrents"
STOP_TIMEOUT = 60
MAX_CONCURRENT = 16
MAX_MAGNETS = 256

ARIA2RPC_ADDR = os.environ["ARIA2RPC_HOST"] if "ARIA2RPC_HOST" in os.environ else "127.0.0.1"
ARIA2RPC_PORT = os.environ["ARIA2RPC_PORT"] if "ARIA2RPC_PORT" in os.environ else 6800

rd = RedisClient()
logger = get_logger("logger_magnet_to_torrent")

def get_magnets():
    """
    获取磁力链接
    """
    mgs = rd.get_magnets(MAX_MAGNETS)
    for m in mgs:
        # 解码成字符串
        yield m.decode()


def exec_rpc(magnet):
    """
    使用 rpc，减少线程资源占用，关于这部分的详细信息科参考
    https://aria2.github.io/manual/en/html/aria2c.html?highlight=enable%20rpc#aria2.addUri
    """
    conn = HTTPConnection(ARIA2RPC_ADDR, ARIA2RPC_PORT)
    req = {
        "jsonrpc": "2.0",
        "id": "magnet",
        "method": "aria2.addUri",
        "params": [
            [magnet],
            {
                "bt-stop-timeout": str(STOP_TIMEOUT),
                "max-concurrent-downloads": str(MAX_CONCURRENT),
                "listen-port": "6881",
                "dir": SAVE_PATH,
            },
        ],
    }
    conn.request(
        "POST", "/jsonrpc", json.dumps(req), {"Content-Type": "application/json"}
    )

    res = json.loads(conn.getresponse().read())
    if "error" in res:
        logger.info("Aria2c replied with an error:{}".format(res["error"]))
    else:
        logger.info("magnet to torrent:{}".format(magnet))
        rd.del_magnet(magnet)


def magnet2torrent():
    """
    磁力转种子
    """
    logger.info("magnet to torrent forever...")
    while True:
        try:
            if rd.count():
                for magnet in get_magnets():
                    exec_rpc(magnet)
                
                time.sleep(SLEEP_TIME_PARSEING)
            else:
                time.sleep(SLEEP_TIME_IDEL)
        except Exception as e:
            logger.exception(e)
