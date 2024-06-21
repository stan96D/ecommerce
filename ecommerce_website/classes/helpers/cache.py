import time


class Cache:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Cache, cls).__new__(cls, *args, **kwargs)
            cls._instance._cache = {}
            cls._instance._expiry_times = {}
        return cls._instance

    def set(self, key, value, ttl):
        self._cache[key] = value
        self._expiry_times[key] = time.time() + ttl
        print(f"Cache set: {key}, expires in {ttl} seconds")

    def get(self, key):
        if key in self._cache and time.time() < self._expiry_times[key]:
            print(f"Cache hit: {key}")
            return self._cache[key]
        if key in self._cache:
            print(f"Cache expired: {key}")
            del self._cache[key]
            del self._expiry_times[key]
        print(f"Cache miss: {key}")
        return None

    def clear(self, key):
        if key in self._cache:
            print(f"Cache cleared: {key}")
            del self._cache[key]
            del self._expiry_times[key]

    def clear_all(self):
        self._cache.clear()
        self._expiry_times.clear()
        print("All cache cleared")
