"""
THEA KERNEL
created: may/10/2018

Founding principles:
* Command line and web friendly API

"""
class Bean:
    def __init__(self, **params):
        self.dat = params
    
    def get(self, key):
        return self.dat[key]

    def set(self, key, val):
        self.dat[key] = val

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


"""

"""