#!/usr/bin/env python3
"""defines a class Cache"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    """Tracks number of calls made to a method in Cache class"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the decorator"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """keeps track of the inputs and output of a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorator"""
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
    """display history of a method call with it's inputs and outputs"""
    redis_client = method.__self__._redis  # Access the Redis instance
    method_name = method.__qualname__

    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"

    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode('utf-8')}) \
              -> {out.decode('utf-8')}")


class Cache():
    """Represents a Cache object for storing data in redis db"""
    def __init__(self) -> None:
        """innitializes a Cache object"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
        return self.get(key, lambda x: x.decode('utf-8'))  # type: ignore

    def get_int(self, key: str) -> int:
        """gets an integer value from a redis data store
        Args:
            key(int): the key to retrieve value
        Return:
            int: the value
        """
        return self.get(key, lambda x: int(x))  # type: ignore
