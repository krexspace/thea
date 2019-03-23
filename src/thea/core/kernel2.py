"""
THEA KERNEL
created: may/10/2018

Founding principles:
* Command line and web friendly API

"""
import thea.core.commands as cm
import copy
import thea.core.utils as ut

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
        ut.log('Graph object initialized')
        super().__init__(**params)

    def delete_all(self):
        ut.log('delete_all')
        cm.cmd_delete_all(None)
    
    def list(self, nodes):
        resp = []
        for n in nodes:
            resp.append(n.dat)
        return resp

    def find(self, **params):
        ut.log('In g.f()')
        resp = cm.cmd_find_by(params)
        nlist = []
        for rec in resp['list']:
            nd = Node(e=True)
            nd.dat = rec
            nlist.append(nd)
        return nlist
    
    def find_one(self, **params):
        resp = self.find(**params)
        if len(resp) > 1:
            raise Exception('More than one Node found. Use f()')
        elif len(resp) == 0:
            return None
        return resp[0]

    # Create connection between node objects n1->n2
    def connect(n1, n2, st=50, ctype=None):
        n1.create_conn_out(n2, st, ctype)

    ''' ---- special and readymade nodes ---- '''
    def node(self, **params):
        n = Node(**params)
        return n
    
    def node_quick(self, title, **params):
        p = dict(title=title)
        p = {**p, **params}
        n = Node(**p)
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
    
    def image(self, src, **params):
        p = dict(src=src, type='img')
        p = {**p, **params}
        n = Node(**p)
        return n
    
    # internally or locally located with same type as above
    def image_int(self, src, dom='domx', **params):
        p = dict(src=src, dom=dom, internal=True, type='img')
        p = {**p, **params}
        n = Node(**p)
        return n
        
    def video(self, src, **params):
        p = dict(src=src, type='vid')
        p = {**p, **params}
        n = Node(**p)
        return n

    # internally or locally located with same type as above
    def video_int(self, src, dom='domx', **params):
        p = dict(src=src, dom=dom, internal=True, type='vid')
        p = {**p, **params}
        n = Node(**p)
        return n

    def audio(self, src, **params):
        p = dict(src=src, type='aud')
        p = {**p, **params}
        n = Node(**p)
        return n
    
    # internally or locally located with same type as above
    def audio_int(self, src, dom='domx', **params):
        p = dict(src=src, dom=dom, internal=True, type='aud')
        p = {**p, **params}
        n = Node(**p)
        return n

    # file is not used as it might be a key word
    def file_remote(self, src, **params):
        p = dict(src=src, type='file')
        p = {**p, **params}
        n = Node(**p)
        return n
    
    # internally located with same type as above
    def file_int(self, src, dom='domx', **params):
        p = dict(src=src, dom=dom, internal=True, type='file')
        p = {**p, **params}
        n = Node(**p)
        return n

    def youtube(self, url, **params):
        p = dict(url=url, type='yt')
        p = {**p, **params}
        n = Node(**p)
        return n

    def thought(self, title, **params):
        p = dict(title=title, type='th')
        p = {**p, **params}
        n = Node(**p)
        return n

    def link(self, url, title=None, **params):
        title = url if title is None else title
        p = dict(url=url, title=title, type='lnk')
        p = {**p, **params}
        n = Node(**p)
        return n

    def logic(self, code, **params):
        p = dict(code=code, type='logic')
        p = {**p, **params}
        n = Node(**p)
        return n
    ''' -- end -> special readymade nodes -- '''

'''
@deprecated remove; since sessions can be created in the graph itself
class Session(Bean):
    def __init__(self, **params):
        ut.log('Session created')
        super().__init__(**params)
'''

class Node(Bean):
    def __init__(self, **params):
        if 'e' not in params or params['e'] != True:
            super().__init__(**params)
            resp = cm.cmd_create_node(copy.deepcopy(self.dat))
            self.__err(resp)
            self.dat['nid'] = resp['val']
        self.onodes = None
        self.inodes = None
    
    def get_out_nodes(self):
        return self.onodes

    def clear_out_nodes(self):
        self.onodes = None
        return self
    
    # Set attributes and save right away
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
    
    # Remove or delete self
    def delete(self):
        self.__isLive()
        resp = cm.cmd_delete_node(self.dat)
        self.__err(resp)
        self.dat = None
        return None
    
    # refresh self values from db, out nodes are not fetched
    def refresh(self):
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
        lonodes = ', num onodes-> {}'.format(len(self.onodes)) if self.onodes is not None else ''
        linodes = ', num inodes-> {}'.format(len(self.inodes)) if self.inodes is not None else ''
        return 'node-> {}{}{}'.format(str(self.dat), lonodes, linodes)

    def print(self):
        ut.log(self.__repr__())
        return self

    # Create outgoing links or connections
    def create_conn_out(self, n, st=50, ctype=None):
        cm.cmd_create_conn({'src':self.dat['nid'],'dest':n.dat['nid'],'st':st,'type':ctype})
        return self

    # Create incoming links or connections
    def create_conn_in(self, n, st=50, ctype=None):
        cm.cmd_create_conn({'dest':self.dat['nid'],'src':n.dat['nid'],'st':st,'type':ctype})
        return self

    # out links or connections (and not nodes)
    def get_out_conns(self, dest_node, ctype=None):
        dest = dest_node.dat['nid']
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

    # out link or single child - single, only connection (and not node)
    def get_out_conn(self, dest_node, ctype=None):
        resp = self.get_out_conns(dest_node, ctype)
        if len(resp) > 1:
            raise Exception('More than one connection detected. Use get_out_conns()')
        elif len(resp) == 0:
            return None
        return resp[0]
        
    # in links and not nodes``
    def get_in_conns(self,src_node, ctype=None):
        src = src_node.dat['nid']
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
    
    # in link or parent - single only
    def get_in_conn(self, src_node, ctype=None):
        resp = self.get_in_conns(src_node, ctype)
        if len(resp) > 1:
            raise Exception('More than one connection detected. Use get_in_conns()')
        elif len(resp) == 0:
            return None
        return resp[0]

    # Get child nodes, in other words get the out connected nodes
    def get_out_nodes(self, ctype=None):
        sub_nids = self.fetch_child_nodes_and_conns(ctype)
        resp = cm.fetch_multi_nodes_by_nid(list(sub_nids[0]))
        nlist = []
        for rec in resp:
            nd = Node(e=True)
            nd.dat = rec
            nlist.append(nd)
        return nlist
    
    # Get child nodes, in other words get the out connected nodes
    def grow(self, ctype=None):
        self.onodes = self.get_out_nodes(ctype)
        return self

    # recursive grow
    def grow_deep(self, ctype=None):
        cnodes = self.grow(ctype).onodes
        for cnode in cnodes:
            cnode.grow_deep(ctype)
        return self


    ''' ---- public util functions ---- '''
    '''
    Giving ctype returns out connected nodes with the given
    connection type
    '''
    def fetch_child_nodes_and_conns(self, ctype=None):
        resp = cm.fetch_child_nodes_and_conns(self.dat['nid'], ctype)
        return resp[1], resp[2]

    '''
    Giving ctype returns out connected sub tree of nodes with the given
    connection type in the immediate sub nodes graph.
    '''
    def fetch_node_tree(self, ctype=None):
        resp = cm.fetch_node_tree(self.dat['nid'], ctype)
        return resp[1], resp[2]



''' Conns don't have a create method '''
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

    def delete(self):
        self.__isLive()
        resp = cm.cmd_delete_conn(self.dat)
        self.__err(resp)
        self.dat = None
        return None
    
    def __err(self, resp):
        if resp is not None and 'err' in resp:
            raise Exception(str(resp['msg']))