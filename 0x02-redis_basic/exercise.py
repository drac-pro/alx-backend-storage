#!/usr/bin/env python3
"""defines a class Cache"""
import redis
import uuid
from typing import Union, Callable


class Cache():
    """Represents a Cache object for storing data in redis db"""
    def __init__(self) -> None:
        """innitializes a Cache object"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """gets a value from the redis db base on it's key
        Args:
            key(str): the key
            fn(Callable): func to convert the value from bytes
        """
        byte_value = self._redis.get(key)
        return fn(byte_value) if fn is not None else byte_value

    def get_str(self, key: str) -> str:
        """gets a string value from a redis data store
        Args:
            key(str): the key to retrieve value
        Return:
            str: the value
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """gets an integer value from a redis data store
        Args:
            key(int): the key to retrieve value
        Return:
            int: the value
        """
        return self.get(key, lambda x: int(x))
