
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

    __unread: int
    __cread: int
    __mutex: Semaphore

    def __init__(self, val: any) -> None:
        self._val = deepcopy(val)
        self.__unread = 0
        self.__cread = 0
        self.__mutex = Semaphore(1)

    # Register a listener to the buffer
    def register(self) -> None:
        self.__mutex.acquire()
        self.__cread += 1
        self.__mutex.release()

    # Unregister a listener from the buffer
    def unregister(self) -> None:
        self.__mutex.acquire()
        self.__cread -= 1
        self.__mutex.release()

    def get_val(self, id: int) -> any:
        val = None
        if id == 1:
            self.__mutex.acquire()
            val = deepcopy(self._val)
            self.__unread -= 1
            self.__mutex.release()
        # if not registered, return the value
        else:
            val = deepcopy(self._val)
        return val
    
    def set_val(self, val: any) -> None:
        while True:
            self.__mutex.acquire()
            if self.__unread > 0:
                self.__mutex.release()
                sleep(0.01*self.__unread)
            else: 
                break
        self._val = deepcopy(val)
        self.__unread = self.__cread
        self.__mutex.release()
