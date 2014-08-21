
__all__ = ["execute", "TangoWorker"]

import logging
import threading
try:
    from queue import Queue
except ImportError:
    from Queue import Queue

class _TangoWorker(threading.Thread):

    def __init__(self, **kwargs):
        kwargs['name'] = kwargs.pop('name', 'TangoWorker')
        daemon = kwargs.pop('daemon', True)
        threading.Thread.__init__(self, **kwargs)
        self.__stop = False
        self.setDaemon(daemon)
        self.tasks = Queue()

    def run(self):
        tasks = self.tasks
        while not self.__stop:
            try:
                f, args, kwargs = tasks.get(timeout=0.5)
            except Queue.Empty:
                continue
            if f is None:
                continue
            try:
                f(*args, **kwargs)
            except:
                logging.warning("Failed to execute %s", str(f))
                logging.warning("Details:", exc_info=1)

    def execute(self, f, *args, **kwargs):
        self.tasks.put((f, args, kwargs))

    def stop(self, wait=False):
        self.__stop = True
        self.execute(None)
        if wait:
            self.join()


__TANGO_WORKER = None
def TangoWorker():
    global __TANGO_WORKER
    if __TANGO_WORKER is None:
        __TANGO_WORKER = _TangoWorker()
        __TANGO_WORKER.start()
    return __TANGO_WORKER


def execute(f, *args, **kwargs):
    """Helper to execute a task in the tango worker thread"""
    return TangoWorker().execute(f, *args, **kwargs)


def stop(wait=False):
    return TangoWorker().stop(wait=wait)


if __name__ == "__main__":

    def f():
        print("Writting message from thread " + threading.current_thread().name)
    
    import sys
    print("Tango worker will write message to stdout...")
    execute(f)
    print("Finished. This message may come before or after the 'Writting message from thread' ...")
    stop(wait=True)
    
    
