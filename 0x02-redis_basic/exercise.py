#!/usr/bin/env python3
""" Redis Basics' module"""
import redis
import uuid
from typing import Union, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator that increments a key in Redis every
    time the decorated function is called
    """
    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator that stores the history
    of inputs and outputs for a function
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_data = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_data)
        output_data = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_data)
        return output_data
    return wrapper


class Cache:
    """ Cache class """

    def __init__(self) -> None:
        """ Class Initializer """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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


def replay(method: Callable) -> None:
    """ 
    Displays the history of calls of a function
    """
    redis_instance = redis.Redis()
    method_name = method.__qualname__
    inputs = redis_instance.lrange(method_name + ":inputs", 0, -1)
    outputs = redis_instance.lrange(method_name + ":outputs", 0, -1)
    print(f"{method_name} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method_name}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")
