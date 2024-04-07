
from threading import Semaphore
from copy import deepcopy
from time import sleep  


class Ref:
    _val: any

    def __init__(self, val: any) -> None:
        self._val = deepcopy(val)

    def get_val(self) -> any:
        return deepcopy(self._val)
    
    def set_val(self, val: any) -> None:
        self._val = deepcopy(val)


class Buffer:

    _val: any

    __listeners: dict[int, Semaphore]
    __unread: int
    __cread: int
    __mutex: Semaphore

    def __init__(self, val: any) -> None:
        self._val = deepcopy(val)
        self.__listeners = dict()
        self.__unread = 0
        self.__cread = 0
        self.__mutex = Semaphore(1)

    # Register a listener to the buffer
    def register(self, id: int) -> None:
        self.__mutex.acquire()
        if id not in self.__listeners:
            self.__listeners[id] = Semaphore(0)
            self.__cread += 1
        self.__mutex.release()

    # Unregister a listener from the buffer
    def unregister(self, id: int) -> None:
        self.__mutex.acquire()
        if id in self.__listeners:
            del self.__listeners[id]
            self.__cread -= 1
        self.__mutex.release()


    def get_val(self, id: int) -> any:
        val = None
        if id in self.__listeners:
            self.__listeners[id].acquire()
            val = deepcopy(self._val)
        self.__mutex.acquire()
        self.__unread -= 1
        self.__mutex.release()
        return val
    
    def set_val(self, val: any) -> None:
        while True:
            if self.__unread > 0:
                sleep(0.01*self.__unread)
                continue
            break
        self.__mutex.acquire()
        self._val = val
        self.__unread = self.__cread
        self.__mutex.release()
        for listener in self.__listeners:
            self.__listeners[listener].release()
