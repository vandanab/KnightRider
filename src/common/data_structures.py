'''
Created on Oct 2, 2012

@author: vandana
Contains basic data structure wrappers.
'''

from abc import abstractmethod, ABCMeta
from collections import deque
from sets import Set
from pymongo import Connection
from settings import DB_SERVER, DB_PORT, CRAWLER_DB_NAME
import threading

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

class MongoQueue(IQueue, ISet):
  """
  mongo db based queue
  """
  def __init__(self, queue_name, elts_list=None):
    self.connection = Connection(DB_SERVER, DB_PORT)
    self.db = self.connection[CRAWLER_DB_NAME]
    self.queue_name = queue_name
    if elts_list:
      for i in elts_list:
        self.db[self.queue_name].insert({"_id": i})
    self.lock_ = threading.RLock()
  
  def dequeue(self):
    with self.lock_:
      item = self.db[self.queue_name].find_one()
      if item:
        self.db[self.queue_name].remove(item)
        return item["_id"]
      return None
  
  def enqueue(self, elt):
    with self.lock_:
      self.db[self.queue_name].insert({"_id": elt})
  
  def extend(self, elts_list):
    with self.lock_:
      for elt in elts_list:
        self.db[self.queue_name].insert({"_id": elt})
  
  def clear(self):
    with self.lock_:
      self.db[self.queue_name].remove({})
  
  def drop(self):
    self.connection.drop_database(self.db)
  
  def iterator(self):
    next_item = True
    while next_item:
      next_item = self.dequeue()
      if next_item: yield next_item
  
  def get_items(self):
    return [item["_id"] for item in self.db[self.queue_name].find()]
  
  def add(self, elt):
    self.enqueue(elt)
  
  def remove(self, elt):
    with self.lock_:
      self.db[self.queue_name].remove({"_id": elt})

  def __contains__(self, key):
    with self.lock_:
      item = self.db[self.queue_name].find({"_id": key})
      if item: return True
      else: return False
  
  def __str__(self):
    elts = self.db[self.queue_name].find()
    return elts.__str__()
        
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
