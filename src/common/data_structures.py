'''
Created on Oct 2, 2012

@author: vandana
Contains basic data structure wrappers.
'''

from abc import abstractmethod, ABCMeta
from collections import deque
from sets import Set

class LUOQueue:
    """
    Look Up Optimized Queue
    """
    def __init__(self, elts_list=None):
        # For a different implementation of IQueue and ISet need to instantiate
        # those classes instead of NativeQueue and NativeSet
        self.queue = NativeQueue(elts_list)
        self.hashset = NativeSet(elts_list)
    
    def enqueue(self, elt):
        self.queue.enqueue(elt)
        self.hashset.add(elt)
    
    def dequeue(self):
        elt = self.queue.dequeue()
        self.hashset.remove(elt)
        return elt
    
    def extend(self, elts_list):
        self.queue.extend(elts_list)
        self.hashset.extend(elts_list)
    
    def clear(self):
        self.queue.clear()
        self.hashset.clear()
    
    def __contains__(self, key):
        return (key in self.hashset)
    
    def __str__(self):
        return self.queue.__str__()

#-------------------------------------------------------------------------

class ISet:
    """
    Set Interface
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def add(self, elt):
        raise NotImplementedError
    
    @abstractmethod
    def remove(self, elt):
        raise NotImplementedError
    
    @abstractmethod
    def extend(self, elts_list):
        raise NotImplementedError
    
    @abstractmethod
    def clear(self):
        raise NotImplementedError
    
    @abstractmethod
    def __contains__(self, key):
        raise NotImplementedError
    
    @abstractmethod
    def __str__(self):
        raise NotImplementedError


class NativeSet(ISet):
    """
    A set is optimized for look ups
    Implemented using python Set
    TODO: Convert to mongo db based Set
    """
    def __init__(self, elts_list=None):
        if elts_list:
            self.elements = Set(elts_list)
        else:
            self.elements = Set()
    
    def add(self, elt):
        self.elements.add(elt)
    
    def remove(self, elt):
        self.elements.remove(elt)
    
    def extend(self, elts_list):
        self.elements.update(elts_list)
    
    def clear(self):
        self.elements.clear()
    
    def __contains__(self, key):
        return (key in self.elements)
    
    def __str__(self):
        print self.elements

#TODO: Write mongo db based queue

#-------------------------------------------------------------------------

class IQueue:
    """
    Queue Interface
    """
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def enqueue(self, elt):
        raise NotImplementedError
    
    @abstractmethod
    def dequeue(self):
        raise NotImplementedError
    
    @abstractmethod
    def extend(self, elts_list):
        raise NotImplementedError
    
    @abstractmethod
    def clear(self):
        raise NotImplementedError
    
    @abstractmethod
    def __str__(self):
        raise NotImplementedError
        
        
class NativeQueue(IQueue):
    """
    Queue implemented using python deque
    """
    def __init__(self, elts_list=None):
        if elts_list:
            self.elements = deque(elts_list)
        else:
            self.elements = deque()
    
    def enqueue(self, elt):
        self.elements.append(elt)
    
    def dequeue(self):
        return self.elements.popleft()
    
    def extend(self, elts_list):
        self.elements.extend(elts_list)
    
    def clear(self):
        self.elements.clear()
    
    def __str__(self):
        return self.elements.__str__()

#TODO: Write mongo db based queue