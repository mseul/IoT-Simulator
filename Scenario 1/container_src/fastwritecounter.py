#3rd-party code by JULIEN DANJOU
#Source: https://julien.danjou.info/atomic-lock-free-counters-in-python/
# and https://github.com/jd/fastcounter
# Used under Apache 2.0 license

import threading
import itertools

class FastWriteCounter(object):
    def __init__(self):
        self._number_of_read = 0
        self._counter = itertools.count()
        self._read_lock = threading.Lock()

    def increment(self):
        next(self._counter)

    def value(self):
        with self._read_lock:
            value = next(self._counter) - self._number_of_read
            self._number_of_read += 1
        return value

