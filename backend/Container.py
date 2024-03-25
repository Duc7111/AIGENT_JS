
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

    __listeners: dict[int, bool]
    __unread: int
    __maxread: int
    __mutex: Semaphore

    def __init__(self, val: any) -> None:
        self._val = deepcopy(val)
        self.__listeners = dict()
        self.__unread = 0
        self.__maxread = 0
        self.__mutex = Semaphore(1)

    # Register a listener to the buffer
    def register(self, id: int) -> None:
        self.__mutex.acquire()
        if id not in self.__listeners:
            self.__listeners[id] = True
            self.__maxread += 1
        self.__mutex.release()

    # Unregister a listener from the buffer
    def unregister(self, id: int) -> None:
        self.__mutex.acquire()
        if id in self.__listeners:
            del self.__listeners[id]
            self.__maxread -= 1
        self.__mutex.release()


    def get_val(self, id: int) -> any:
        self.__mutex.acquire()
        if id in self.__listeners and self.__listeners[id]:
            self.__unread -= 1
            self.__listeners[id] = False
            val = deepcopy(self._val)
        self.__mutex.release()
        return val
    
    def set_val(self, val: any) -> None:
        while True:
            self.__mutex.acquire()
            if self.__unread > 0:
                self.__mutex.release()
                sleep(0.03) 
                continue
            break
        self._val = deepcopy(val)
        self.__unread = self.__maxread
        for listener in self.__listeners:
            self.__listeners[listener] = True
        self.__mutex.release()
