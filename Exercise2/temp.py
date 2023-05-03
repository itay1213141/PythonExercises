import threading

class Stream:
    def __init__(self):
        self.list = []
        self.action = None
        self.stopped = False
        
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while not self.stopped:
            with self.lock:
                if self.list and self.action:
                    self.action()
                elif not self.list:
                    self.action = None
    
    def add(self, item):
        with self.lock:
            self.list.append(item)

    def apply(self, func):
        new_stream = Stream()
        
        def action():
            while not self.stopped:
                with self.lock:
                    if self.list:
                        item = self.list.pop(0)
                    else:
                        continue
                    
                result = func(item)
                if result is True:
                    new_stream.add(item)
                elif result is not None:
                    new_stream.add(result)
        
        self.action = action
        return new_stream

    def forEach(self, func):
        def action():
            while not self.stopped:
                with self.lock:
                    if self.list:
                        item = self.list.pop(0)
                    else:
                        continue
                    
                func(item)
                
        self.action = action
        

    def stop(self):
        self.stopped = True
        self.thread.join()