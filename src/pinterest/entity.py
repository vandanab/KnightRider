'''
Created on Oct 2, 2012

@author: vandana
Base class for pinterest entities.
'''
class Entity:
    def __init__(self, url):
        self.url = url
    
    def get_json(self):
        """
        Convert the object to json.
        """
        raise NotImplementedError