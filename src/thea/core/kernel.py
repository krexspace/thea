"""
THEA KERNEL
created: may/10/2018

Founding principles:
* Command line and web friendly API

"""
import thea.core.commands as cm
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

    def delete_all(self):
        cm.cmd_delete_all(None)

    def f(self, **params):
        resp = cm.cmd_find_by(params)
        nlist = []
        for rec in resp['list']:
            nd = Node(e=True)
            nd.dat = rec
            nlist.append(nd)
        return nlist
    
    def fo(self, **params):
        resp = self.f(**params)
        if len(resp) > 1:
            raise Exception('More than one Node found. Use f()')
        elif len(resp) == 0:
            return None
        return resp[0]

    def cn(self, **params):
        n = Node(**params)
        return n

    def realm(self, title, **params):
        p = dict(title=title, type='rlm')
        p = {**p, **params}
        n = Node(**p)
        return n

    def cluster(self, title, **params):
        p = dict(title=title, type='cl')
        p = {**p, **params}
        n = Node(**p)
        return n

    def note(self, title, **params):
        p = dict(title=title, type='note')
        p = {**p, **params}
        n = Node(**p)
        return n
    
    def idea(self, title, **params):
        p = dict(title=title, type='idea')
        p = {**p, **params}
        n = Node(**p)
        return n
    
    def img(self, src, **params):
        p = dict(src=src, type='img')
        p = {**p, **params}
        n = Node(**p)
        return n

    def yt(self, url, **params):
        p = dict(url=url, type='yt')
        p = {**p, **params}
        n = Node(**p)
        return n

    def th(self, title, **params):
        p = dict(title=title, type='th')
        p = {**p, **params}
        n = Node(**p)
        return n

    def lnk(self, url, title, **params):
        title = url if title is None else title
        p = dict(title=title, type='lnk')
        p = {**p, **params}
        n = Node(**p)
        return n

    def clink(n1, n2, st=50, ctype='STD'):
        n1.lo(n2, st, ctype)

class Session(Bean):
    def __init__(self, **params):
        super().__init__(**params)
  
class Node(Bean):
    def __init__(self, **params):
        if 'e' not in params or params['e'] != True:
            super().__init__(**params)
            resp = cm.cmd_create_node(self.dat)
            self.__err(resp)
            self.dat['nid'] = resp['val']
    
    def set(self, **params):
        self.__isLive()
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
    
    # refresh from db
    def refresh(self):
        self.__isLive()
        resp = cm.cmd_find_by({'nid':self.dat['nid']})
        self.dat = resp['list'][0]
        return self

    # same as ref
    def ld(self):
        return self.refresh()

    def __isLive(self):
        if self.dat is None:
            raise Exception("Node is dead")
    
    def __err(self, resp):
        if resp is not None and 'err' in resp:
            raise Exception(str(resp['msg']))

    def __repr__(self):
        return 'node-> ' + str(self.dat)

    # outgoing link or connection
    def clo(self, n, st=50, ctype='STD'):
        cm.cmd_create_conn({'src':self.dat['nid'],'dest':n.dat['nid'],'st':st,'type':ctype})
        return self

    # incoming link or connection
    def cli(self, n, st=50, ctype='STD'):
        cm.cmd_create_conn({'dest':self.dat['nid'],'src':n.dat['nid'],'st':st,'type':ctype})
        return self

    def foutlinksto(self, n, ctype=None):
        dest = n.dat['nid']
        src = self.dat['nid']
        resp  = cm.find_conns(dest=dest, src=src, type=ctype)
        conn_list = []
        for c in resp['val']:
            # copy to cid
            c['cid'] = c['id']
            del c['id']
            c['src'] = src
            c['dest'] = dest
            
            cn = Conn(**c)
            conn_list.append(cn)
        return conn_list

    def foutlinkto(self, n, ctype=None):
        resp = self.foutlinksto(n, ctype)
        if len(resp) > 1:
            raise Exception('More than one connection detected. Use foutlinks()')
        elif len(resp) == 0:
            return None
        return resp[0]

    def finlinksfrom(self, n, ctype=None):
        src = n.dat['nid']
        dest = self.dat['nid']
        resp  = cm.find_conns(dest=dest, src=src, type=ctype)
        conn_list = []
        for c in resp['val']:
            # copy to cid
            c['cid'] = c['id']
            del c['id']
            c['src'] = src
            c['dest'] = dest
            
            cn = Conn(**c)
            conn_list.append(cn)
        return conn_list
    
    def finlinkfrom(self, n, ctype=None):
        resp = self.finlinksfrom(n, ctype)
        if len(resp) > 1:
            raise Exception('More than one connection detected. Use links_finlinksfrom()')
        elif len(resp) == 0:
            return None
        return resp[0]

    def ftree(self, ctype=None):
        clist = cm.fetch_child_nodes_and_conns(self.dat['nid'])
        return clist
    '''
    foutnodes
    finnodes
    finnode
    '''


class Conn(Bean):
    def __repr__(self):
        return 'conn-> ' + str(self.dat)
    
    def set(self, **params):
        self.__isLive()
        super().set(**params)
        self.__sv()
        return self

    def __sv(self):
        self.__isLive()
        resp = cm.cmd_update_conn(copy.deepcopy(self.dat))
        self.__err(resp)
        return self

    def __isLive(self):
        if self.dat is None:
            raise Exception("Conn is dead")

    def rm(self):
        self.__isLive()
        resp = cm.cmd_delete_conn(self.dat)
        self.__err(resp)
        self.dat = None
        return None
    
    def __err(self, resp):
        if resp is not None and 'err' in resp:
            raise Exception(str(resp['msg']))