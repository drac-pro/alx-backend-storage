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
        cache_key = f'cache:{url}'
        count_key = f'count:{url}'
        store.incr(count_key)

        cached_page = store.get(cache_key)
        if cached_page:
            return cached_page.decode('utf-8')

        page = fn(url)
        store.set(count_key, 0)
        store.setex(cache_key, 10, page)
        return page
    return wrapper


@cache_url_req
def get_page(url: str) -> str:
    """returns the html page of a url"""
    return requests.get(url).text
