#!/usr/bin/env python3
""" Redis Basics' module"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(func: Callable) -> Callable:
    """
    Decorator that increments a key in Redis every
    time the decorated function is called
    """
    key = func.__qualname__

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return func(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Cache class """

    def __init__(self) -> None:
        """ Class Initializer """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ 
        Stores the `data` in Redis 

        Args:
            data (str): Data to store

        Returns:
            str: UUID
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Union[None, int, float] = None) -> Union[str, bytes, int, float]:
        """ 
        Retrieves the data stored in Redis

        Args:
            key (str): Key to retrieve
            fn (Union[None, int, float]): Function to cast the data

        Returns:
            Union[str, bytes, int, float]: Data stored in Redis
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ 
        Retrieves the data stored in Redis as string

        Args:
            key (str): Key to retrieve

        Returns:
            str: Data stored in Redis
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """ 
        Retrieves the data stored in Redis as integer

        Args:
            key (str): Key to retrieve

        Returns:
            int: Data stored in Redis
        """
        return self.get(key, int)
