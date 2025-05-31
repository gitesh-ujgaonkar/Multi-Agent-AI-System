import threading

# No import changes needed here; this is the base of the memory module.

class SharedMemory:
    def __init__(self):
        self.memory = []
        self.lock = threading.Lock()

    def log(self, entry: dict):
        with self.lock:
            self.memory.append(entry)

    def snapshot(self):
        with self.lock:
            return list(self.memory) 