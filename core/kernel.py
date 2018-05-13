"""
THEA KERNEL
created: may/10/2018

Founding principles:
* Command line and web friendly API

"""
import commands as cm
import copy

class Bean:
    def __init__(self, **params):
        self.dat = params
    
    def get(self, key):
        return self.dat[key]

    def set(self, **params):
        for key in params: 
            self.dat[key] = params[key]

class Graph(Bean):
    def __init__(self, **params):
        super().__init__(**params)

    def create(self, name):
        self.name = name

class Session(Bean):
    def __init__(self, **params):
        super().__init__(**params)
    
class Node(Bean):
    def __init__(self, **params):
        super().__init__(**params)
        resp = cm.cmd_create_node(self.dat)
        self.__err(resp)
        self.dat['nid'] = resp['val']
    
    def set(self, **params):
        super().set(**params)
        self.__sv()
        return self

    def __sv(self):
        self.__isLive()
        resp = cm.cmd_update_node(copy.deepcopy(self.dat))
        self.__err(resp)
        return self
    
    def rm(self):
        self.__isLive()
        resp = cm.cmd_delete_node(self.dat)
        self.__err(resp)
        self.dat = None
        return None
    
    def ref(self):
        self.__isLive()
        resp = cm.cmd_find_by({'nid':self.dat['nid']})
        self.dat = resp['list'][0]
        return self

    def __isLive(self):
        if self.dat is None:
            raise Exception("Node is dead")
    
    def __err(self, resp):
        if resp is not None and 'err' in resp:
            raise Exception(str(resp['msg']))

    def __repr__(self):
        return 'node-> ' + str(self.dat)