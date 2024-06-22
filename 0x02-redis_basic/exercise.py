#!/usr/bin/env python3
""" Redis Basics' module"""
import redis
import uuid
from typing import Union


class Cache:
    """ Cache class """

    def __init__(self) -> None:
        """ Class Initializer """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
