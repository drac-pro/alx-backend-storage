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
        cached_page = store.get(f'cached:{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        page = fn(url)
        store.setex(f'cached:{url}', 10, page)
        return page
    return wrapper


def get_page(url: str) -> str:
    """returns the html page of a url"""
    return requests.get(url).text
