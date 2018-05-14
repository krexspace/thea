import thea.core.neo as nc
import thea.core.mclient as mongo
import thea.core.utils as ut

neo = nc.GraphDb()

import uuid

"""
To work from command line
import juanix.central_processor as cp

Usage examples
cp.cmd_fetch_all()
cp.cmd_find_by({'kwds':'ideas'})
cp.cmd_find_by({'type':'th'})
cp.cmd_create_node({'title':'Great experiences', 'kwds':'fun,experience,bliss'})
"""

session = {
}

"""
===========================================================================
COMMON UTIL FUNCTIONS
===========================================================================
"""

def notList(arg):
    return type(arg) is not list

def checkKwds(cparams):
    return 'kwds' in cparams and notList(cparams['kwds'])
    
def checkMarkers(cparams):
    return 'markers' in cparams and notList(cparams['markers'])


def gen_uuid():
    return str(uuid.uuid4())

'''
def parse_neo_resp(resp):
    e = False
    if resp[0] != 0:
        e = True
    return {'err': e, 'list_data': resp[1]}


def parse_neo_resp_list(resp):
    e = False
    resp_list = []
    if resp[0] != 0:
        e = True
    for rec in resp[1]['results'][0]['data']:
        resp_list.append(rec['row'][0])
    return {'err': e, 'data': resp_list}
'''

"""
===========================================================================
COMMAND FUNCTIONS
===========================================================================

response contract:

list for Arrays
val for strings, numbers, booleans
obj for JSON

err: True for errors
msg: For errors
"""

def create_node(**cparams):
    return cmd_create_node(cparams)

def cmd_create_node(cparams):
    try:
        ut.log('In cmd_create_node:', cparams)
        # cparams['nid'] = gen_uuid()
        if 'type' not in cparams:
            cparams['type'] = 'th'
        if 'zone' not in cparams:
            cparams['zone'] = 'std'
        if checkKwds(cparams):
            kwds_str = cparams['kwds']
            kwds = kwds_str.split(',')
            del cparams['kwds']
            cparams['kwds'] = kwds
        if checkMarkers(cparams):
            m_str = cparams['markers']
            m = m_str.split(',')
            del cparams['markers']
            cparams['markers'] = m

        # MONGO INSERT
        mresp = mongo.insert(cparams)
        if mresp[0] is True:
            return {'err': True, 'msg': '[MONGO CLIENT EXCEPTION]' + mresp[1]}
        else:
            neorec = {'nid': str(mresp[1].inserted_id)}

            # NEO INSERT
            resp = neo.insert_node(neorec)
            #if resp[0] != 0:
            #    raise Exception(str(resp))
            return {'val': str(mresp[1].inserted_id)}
    except Exception as e:
        return {'err': True, 'msg': str(e)}


def update_node(**cparams):
    return cmd_update_node(cparams)
def cmd_update_node(cparams):
    try:
        ut.log('In cmd_update_node:', cparams)
        if 'nid' not in cparams:
            raise Exception('nid is required to update')
        if 'type' not in cparams:
            cparams['type'] = 'th'
        if 'zone' not in cparams:
            cparams['zone'] = 'std'
        if checkKwds(cparams):
            kwds_str = cparams['kwds']
            kwds = kwds_str.split(',')
            del cparams['kwds']
            cparams['kwds'] = kwds
        if checkMarkers(cparams):
            m_str = cparams['markers']
            m = m_str.split(',')
            del cparams['markers']
            cparams['markers'] = m
        # Expects nid to update
        mresp = mongo.update(cparams)
        #ut.log(mresp[1])
        if mresp[0] is True:
            return {'err': True, 'msg': '[MONGO CLIENT EXCEPTION]' + mresp[1]}
        else:
            # No need to inser to Neo
            return {'val': 'SUCCESS'}
    except Exception as e:
        return {'err': True, 'msg': str(e)}


def find_all(**cparams):
    return cmd_find_all(cparams)
def cmd_find_all(cparams=None):
    ut.log('In cmd_fetch_all:', cparams)
    """
    limit = 100
    if cparams is not None and 'limit' in cparams:
        limit = cparams['limit']
    resp = neo.select_all(int(limit))
    p_resp = parse_neo_resp_list(resp)
    """
    resp = mongo.read(cparams)
    if resp[0] is True:
        return {'err': True, 'msg': resp[1]}
    else:
        flist = []
        for r in resp[1]:
            r['nid'] = str(r['_id'])
            del r['_id']
            flist.append(r)
        return {'list': flist}


def find_by(**cparams):
    return cmd_find_by(cparams)
def cmd_find_by(cparams):
    ut.log('In cmd_find_by:', cparams)
    """
    limit = 100
    if cparams is not None and 'limit' in cparams:
        limit = cparams['limit']
    resp = neo.select_all(int(limit))
    p_resp = parse_neo_resp_list(resp)
    """

    if checkKwds(cparams):
        kwds_str = cparams['kwds']
        kwds = kwds_str.split(',')
        del cparams['kwds']
        cparams['kwds'] = {'$in': kwds}

    if checkMarkers(cparams):
        kwds_str = cparams['markers']
        kwds = kwds_str.split(',')
        del cparams['markers']
        cparams['markers'] = {'$in': kwds}
    ut.log(cparams)
    resp = mongo.read(cparams)
    if resp[0] is True:
        return {'err': True, 'msg': resp[1]}
    else:
        flist = []
        for ritem in resp[1]:
            ritem['nid'] = str(ritem['_id'])
            del ritem['_id']
            flist.append(ritem)
        return {'list': flist}


def delete_all(**cparams):
    return cmd_delete_all(cparams)
def cmd_delete_all(cparams):
    try:
        ut.log('In cmd_delete_all:', cparams)
        neo.delete_all()
        mresp = mongo.delete_all()
        return {'val': "SUCCESS"}

    except Exception as e:
        return {'err': True, 'msg': str(e)}


def delete_node(**cparams):
    return cmd_delete_node(cparams)
def cmd_delete_node(cparams):
    ut.log('In cmd_delete_one:', cparams)
    neo.delete_by_nid(cparams['nid'])
    #if nresp[0] != 0:
    #    raise Exception(str(nresp))
    mresp = mongo.delete_one(cparams)
    if mresp[0] is True:
        return {'err': True, 'msg': mresp[1]}
    else:
        return {'val': str(mresp[1].deleted_count)}


def create_conn(**cparams):
    return cmd_create_conn(cparams)
def cmd_create_conn(cparams):
    try:
        ctype = 'STD'
        st = 50
        if 'type' in cparams:
            ctype = cparams['type']
        if 'st' in cparams:
            st = cparams['st']
        resp = neo.insert_rel_by_nid(cparams['src'], cparams['dest'], st, ctype, 1)
        ut.log(resp)
        return {'val': resp}
    except Exception as e:
        return {'err': True, 'msg': str(e)}


def find_conns(**cparams):
    return cmd_find_conns(cparams)
def cmd_find_conns(cparams):
    try:
        ctype = None # Ignores type
        if 'type' in cparams:
            ctype = cparams['type']
        if 'st' in cparams:
            st = cparams['st']
        resp = neo.find_all_out_relations(cparams['src'], cparams['dest'], ctype)
        return {'val': resp}
    except Exception as e:
        return {'err': True, 'msg': str(e)}


def update_conn(**cparams):
    return cmd_update_conn(cparams)
# To update conn it is dropped and recreated
# Update is by cid
# You can update strenth and type of the conn
def cmd_update_conn(cparams):
    try:
        resp = neo.update_rel_by_relid(cparams['cid'], cparams['st'], cparams['type'])
    except Exception as e:
        return {'err': True, 'msg': str(e)}


def delete_conn(**cparams):
    return cmd_delete_conn(cparams)
# If type is not sent in all connections will be dropped
# Delete by connection ID or delete by connected nodes
# If delete is by node ids - src and dest (and optionally type of conn)
def cmd_delete_conn(cparams):
    try:
        # cid takes priority if sent
        if 'cid' in cparams:
            resp = neo.delete_rel_by_relid(cparams['cid'])
        else:
            ctype = None
            if 'type' in cparams:
                ctype = cparams['type']
            # If type is not sent in all connections will be dropped
            if ctype is None:
                resp = neo.delete_all_rel_by_nid(cparams['src'], cparams['dest'])
            else:
                resp = neo.delete_rel_by_nid(cparams['src'], cparams['dest'], ctype)
                
        return {'val': resp}   
    except Exception as e:
        return {'err': True, 'msg': str(e)}


def cmd_create_session(cparams):
    sid = gen_uuid()
    session[sid] = {}
    return {'val': sid}


def cmd_delete_session(cparams):
    sid = cparams['sid']
    session.pop(sid, None)
    return {'val': 'SUCCESS'}


def cmd_fetch_tree(cparams):
    try:
        nid = cparams['nid']
        #ut.log(nid)
        res = fetch_node_tree(nid)
        #ut.log('fetch res:', {'nodes': list(res[1]), 'conns': res[2]})
        resp = {'obj': {'nodes': list(res[1]), 'conns': res[2], 'view_id':'node_graph'}}
        #ut.log('service resp', resp)
        return resp
    except Exception as ex:
        return {'err': True, 'msg': str(ex)}
    except:
        return {'err': True, 'msg': 'Error fetching node tree data'}


"""
===========================================================================
INTERNAL COMMAND UTIL FUNCTIONS
===========================================================================
"""

"""
Currently uses recursion and multiple child calls.abs This can be 
optimized at the NEO layer to fetch everything in one go, and at MONGO layer by sending multiple 

"""
def fetch_node_tree(rootNid, cytpe=None, lev=10):
    level = 0
    maxLev = lev
    nodes = set()
    conns = []
    fetch_node_tree_inner(rootNid, level, nodes, conns, maxLev, cytpe)
    return 0, nodes, conns

# RECURSIVE
def fetch_node_tree_inner(nid, level, nodes, conns, maxLev=10, cytpe=None):
    level += 1
    if level <= maxLev:
        res = fetch_child_nodes_and_conns(nid, cytpe)
        cnodes = res[1]
        if len(cnodes) > 0:
            nodes.update(cnodes)
            #ut.log(level, cnodes)
            cconns = res[2]
            conns.extend(cconns)
            #ut.log(level, cconns)
            for sub_node in cnodes:
                fetch_node_tree_inner(sub_node, level, nodes, conns, maxLev, cytpe)
    else:
        return None


def fetch_child_nodes_and_conns(nid, ctype=None):
    nodes = set()
    conns = []
    res = neo.find_all_out_related_nodes(nid, ctype, True)
    # print(res)
    for k in res:
        dest_nid = k['nid']
        conn_str = k['st']
        conn_type = k['type']
        conn_id = k['id']
        nodes.add(dest_nid)
        conn = dict(cid=conn_id, type=conn_type, st=conn_str, src=nid, dest=dest_nid)
        conns.append(conn)
    return 0, nodes, conns


"""
Suggested:
addto_context
deletefrom_context
clear_context
"""