#!/usr/bin/env python3
"""defines a function get_page"""
import redis
import requests
from functools import wraps
from typing import Callable


store = redis.Redis()


def cache_url_req(fn: Callable) -> Callable:
    """track how many times a particular URL was accessed
    and cache the result with an expiration time of 10 seconds."""
    @wraps(fn)
    def wrapper(url):
        """decorator wrapper"""
        store.incr(f'count:{url}')
        result = store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = fn(url)
        store.set(f'count:{url}', 0)
        store.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_url_req
def get_page(url: str) -> str:
    """returns the html page of a url"""
    return requests.get(url).text
