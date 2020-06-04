#!/usr/bin/env python
# coding=utf-8

import redis
import os

# redis key
REDIS_KEY = os.environ["REDIS_KEY"] if "REDIS_KEY" in os.environ else "magnets"
# redis 地址
REDIS_HOST = os.environ["REDIS_HOST"] if "REDIS_HOST" in os.environ else "localhost"
# redis 端口
REDIS_PORT = os.environ["REDIS_PORT"] if "REDIS_PORT" in os.environ else 6379
# redis 密码
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"] if "REDIS_PASSWORD" in os.environ else None
# redis 连接池最大连接量
REDIS_MAX_CONNECTION = 20


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        conn_pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            max_connections=REDIS_MAX_CONNECTION,
        )
        self.redis = redis.Redis(connection_pool=conn_pool)

    def add_magnet(self, magnet):
        """
        新增磁力链接
        """
        self.redis.sadd(REDIS_KEY, magnet)

    def get_magnets(self, count=128):
        """
        返回指定数量的磁力链接
        """
        return self.redis.srandmember(REDIS_KEY, count)
