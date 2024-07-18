#!/usr/bin/env python3
"""defines a function get_page"""
import redis
import requests
from functools import wraps
from typing import Callable


store = redis.Redis()


def cache_url_req(func: Callable) -> Callable:
    """track how many times a particular URL was accessed
    and cache the result with an expiration time of 10 seconds."""
    @wraps(func)
    def wrapper(url):
        """decorator wrapper"""
        key = "cached:" + url
        cached_value = store.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        key_count = "count:" + url
        html_content = func(url)

        store.incr(key_count)
        store.set(key, html_content, ex=10)
        store.expire(key, 10)
        return html_content
    return wrapper


@cache_url_req
def get_page(url: str) -> str:
    """returns the html page of a url"""
    return requests.get(url).text
