import random

class Die:
    def __init__(self):
        self._value = 1
        self._lock = False

    def set_value(self, value):
        self._value = value
    
    def get_value(self):
        return self._value

    def roll(self):
        self._value = random.randint(1, 6)
        return self._value

    def lock(self):
        self._lock = True

    def unlock(self):
        self._lock = False
    
    def is_locked(self):
        return self._lock