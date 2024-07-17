#!/usr/bin/env python3
"""defines a class Cache"""
import redis
import uuid
from typing import Union


class Cache():
    """"""
    def __init__(self) -> None:
        """innitializes a Cache object"""
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store the input data in Redis using the random key
        and return the key.
        Args:
            data(str|bytes|int|float): data to be stored
        Return:
            uuid: key to stored data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
