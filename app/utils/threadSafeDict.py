from collections import defaultdict
from threading import Lock, Thread
import time

class ThreadSafeDict:
    def __init__(self, ttl=60, cleanup_interval=10):
        self.lock = Lock()
        self.dict = defaultdict()
        self.ttl = ttl  # Time to live for each key-value pair in seconds
        self.cleanup_interval = cleanup_interval  # Interval for cleanup in seconds
        self.timestamps = defaultdict()
        self.cleanup_thread = Thread(target=self._cleanup, daemon=True)
        self.cleanup_thread.start()

    def get(self, key):
        with self.lock:
            if key in self.dict and (time.time() - self.timestamps[key]) < self.ttl:
                return self.dict.get(key)
            elif key in self.dict:
                del self.dict[key]
                del self.timestamps[key]
            return None

    def set(self, key, value):
        with self.lock:
            self.dict[key] = value
            self.timestamps[key] = time.time()

    def delete(self, key):
        with self.lock:
            if key in self.dict:
                del self.dict[key]
                del self.timestamps[key]

    def _cleanup(self):
        while True:
            time.sleep(self.cleanup_interval)
            with self.lock:
                current_time = time.time()
                keys_to_delete = [key for key, timestamp in self.timestamps.items() if (current_time - timestamp) >= self.ttl]
                for key in keys_to_delete:
                    del self.dict[key]
                    del self.timestamps[key]

# 示例使用
if __name__ == "__main__":
    ts_dict = ThreadSafeDict(ttl=5, cleanup_interval=2)
    ts_dict.set("key1", "value1")
    time.sleep(3)
    print(ts_dict.get("key1"))  # 应该输出 "value1"
    time.sleep(3)
    print(ts_dict.get("key1"))  # 应该输出 None，因为已经超过了 TTL