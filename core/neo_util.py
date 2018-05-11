import json
import requests

"""
# Sets the unique constraint
# CREATE CONSTRAINT ON (p:PNODE) ASSERT p.nid IS UNIQUE
"""

# { "query":"' + jsonStripNewlines(cypherQuery) + '","params" : {} }
# reference only
"""
def fire_cypher_legacy(cyp_string):
    url = 'http://neo4j:racipin0@localhost:7474/db/data/cypher'
    json_payload = {
        'query': cyp_string,
        'params': None
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(json_payload), headers=headers)
    return r
"""


def fire_cypher(cyp_string, params):
    url = 'https://@192.168.1.118:7474/db/data/transaction/commit/'
    json_payload = {
        "statements": [{
            "statement": cyp_string,
            "parameters": params
        } ]
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(json_payload), headers=headers)
    return r


# from neo.base import insert_test_1 as in1
def __insert_test_1():
    cyp = 'CREATE (p:Person {name:{name},born:{born}}) ' \
          'RETURN p, ID(p)'
    params = {"name": "Clint Eastwood", "born": 1930}
    r = fire_cypher(cyp, params)

    print(r.json())


# from neo.base import insert_node as ins
def insert_node_nid(nid):
    cyp = 'CREATE (p:PNODE {nid:{nid}}) RETURN p, ID(p)'
    params = {"nid": nid}
    r = fire_cypher(cyp, params)
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        # returns the new id
        return 0, r.json()['results'][0]['data'][0]['row'][1]


# Same as below but expects a dictionary
def insert_node(args):
    # build param string
    print("insert_node", args)
    pstr = ''
    pl = len(args)
    c = 0
    for k, v in args.items():
        pstr += k + ':' + '{' + k + '}'
        c += 1
        if c < pl:
            pstr += ','

    cyp = 'CREATE (p:PNODE {' + pstr + '}) RETURN p, ID(p)'
    params = args
    r = fire_cypher(cyp, params)
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        # returns the new id
        return 0, r.json()['results'][0]['data'][0]['row'][1]


# nb.insert_node(nid='TEST02', title='Cool days', url='http://cool.domain/island')
def insert_node2(**args):
    return insert_node(args)


# from neo.base import insert_rel_by_id as inr
# Here id is the Nodes' native neo ID
def insert_rel_by_id(id1, id2, st):
    cyp = 'MATCH (a:PNODE),(b:PNODE) ' \
          'WHERE ID(a) = {id1} AND ID(b) = {id2} ' \
          'CREATE (a)-[r:NCONN {strength:{st}}]->(b) ' \
          'RETURN r, ID(r)'

    params = {"id1": id1, "id2": id2, "st": st}
    r = fire_cypher(cyp, params)
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        # returns the new id
        return 0, r.json()['results'][0]['data'][0]['row'][1]


# from neo.base import insert_rel_by_nid as inr
# dir 1 is outgoing, 2 is incoming
def insert_rel_by_nid(nid1, nid2, rel_type="STD", st=50, direction=1):
    if direction == 0:
        raise Exception("Bi-directional relationships are not supported")
    elif direction == 1:
        # out going: nid1 -> nid2
        rel_str = '(a)-[r:NCONN {strength:{st},type:{type}}]->(b) '
    elif direction == 2:
        # in coming: nid1 <- nid2
        rel_str = '(a)<-[r:NCONN {strength:{st},type:{type}}]-(b) '
    else:
        raise Exception("Invalid direction")

    cyp = 'MATCH (a:PNODE),(b:PNODE) ' \
          'WHERE a.nid = {nid1} AND b.nid = {nid2} ' \
          'CREATE ' + rel_str +\
          'RETURN r, ID(r)'

    params = {"nid1": nid1, "nid2": nid2, "st": st, "type": rel_type}
    r = fire_cypher(cyp, params)
    # returns the new rel id
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        # returns the new id
        return 0, r.json()['results'][0]['data'][0]['row'][1]


def delete_rel_by_nid(nid1, nid2, rel_type="STD"):

    cyp = 'MATCH (a:PNODE)-[r:NCONN]-(b:PNODE) ' \
          'WHERE a.nid = {nid1} AND b.nid = {nid2} AND r.type = {type} ' \
          'DELETE r'

    params = {"nid1": nid1, "nid2": nid2, "type": rel_type}
    r = fire_cypher(cyp, params)
    # returns the new rel id
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        # returns the new id
        return 0, r.json()

# Delete a relationship by its native neo ID
def delete_rel_by_relid(rel_id):
    cyp = 'MATCH ()-[r:NCONN]-() ' \
          'WHERE ID(r) = {rel_id} ' \
          'DELETE r'

    params = {"rel_id": rel_id}
    r = fire_cypher(cyp, params)
    # returns the new rel id
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        # returns the new id
        return 0, r.json()


# deletes all irrespective of relation type
def delete_all_rel_by_nid(nid1, nid2):

    cyp = 'MATCH (a:PNODE)-[r:NCONN]-(b:PNODE) ' \
          'WHERE a.nid = {nid1} AND b.nid = {nid2} ' \
          'DELETE r'

    params = {"nid1": nid1, "nid2": nid2}
    r = fire_cypher(cyp, params)
    # returns the new rel id
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        # returns the new id
        return 0, r.json()


# from neo.base import delete_all as del_all
def delete_all():
    cyp = 'MATCH (n) DETACH DELETE n'
    params = None
    r = fire_cypher(cyp, params)
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


# delete by nid
def delete_by_nid(nid):
    cyp = 'MATCH (a:PNODE) WHERE a.nid = {nid} DETACH DELETE a'
    params = {"nid": nid}
    r = fire_cypher(cyp, params)
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


# Usage
# n.select_test_1().json()['results'][0]['data']
def select_all(limit=100):
    cyp = 'MATCH (n) RETURN n LIMIT {limit}'
    params = {"limit": limit}
    r = fire_cypher(cyp, params)
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


# rel type and strenth has to be passed or will be reset 
# # to defaults
def update_rel_by_relid(rel_id, rel_type="STD", st=50):
    cyp = 'MATCH ()-[r:NCONN]-() ' \
          'WHERE ID(r) = {rel_id} ' \
          'SET r.strength = {st}, r.type = {rel_type}'

    params = {"rel_id": rel_id, "rel_type": rel_type, "st": st}
    r = fire_cypher(cyp, params)
    # returns the new rel id
    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        # returns the new id
        return 0, r.json()

def find_all_relations(nid1, nid2, rel_type=None):
    rel_str = "" if rel_type is None else "AND r.type = {type} "
    cyp = 'MATCH (a:PNODE)-[r]-(b:PNODE) ' \
          'WHERE a.nid = {nid1} AND b.nid = {nid2} ' + rel_str +\
          'RETURN r, ID(r)'

    params = {"nid1": nid1, "nid2": nid2}
    if rel_type is not None:
        params['type'] = rel_type
    r = fire_cypher(cyp, params)

    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


def find_all_out_relations(nid1, nid2, rel_type=None):
    rel_str = "" if rel_type is None else "AND r.type = {type} "
    cyp = 'MATCH (a:PNODE)-[r]->(b:PNODE) ' \
          'WHERE a.nid = {nid1} AND b.nid = {nid2} ' + rel_str + \
          'RETURN r, ID(r)'

    params = {"nid1": nid1, "nid2": nid2}
    if rel_type is not None:
        params['type'] = rel_type
    r = fire_cypher(cyp, params)

    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


def find_all_in_relations(nid1, nid2, rel_type=None):
    rel_str = "" if rel_type is None else "AND r.type = {type} "
    cyp = 'MATCH (a:PNODE)<-[r]-(b:PNODE) ' \
          'WHERE a.nid = {nid1} AND b.nid = {nid2} ' + rel_str + \
          'RETURN r, ID(r)'

    params = {"nid1": nid1, "nid2": nid2}
    if rel_type is not None:
        params['type'] = rel_type
    r = fire_cypher(cyp, params)

    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


def find_all_related_nodes(nid1, rel_type=None, include_relations=False):
    rel_str = "" if rel_type is None else "AND r.type = {type} "
    inc_rel_str = 'r,' if include_relations else ''
    cyp = 'MATCH (a:PNODE)-[r]-(b:PNODE) ' \
          'WHERE a.nid = {nid1} ' + rel_str + \
          'RETURN DISTINCT b,' + inc_rel_str + 'ID(b)'

    params = {"nid1": nid1}
    if rel_type is not None:
        params['type'] = rel_type
    r = fire_cypher(cyp, params)

    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


def find_all_out_related_nodes(nid1, rel_type=None, include_relations=False):
    rel_str = "" if rel_type is None else "AND r.type = {type} "
    inc_rel_str = 'r,ID(r),' if include_relations else ''
    cyp = 'MATCH (a:PNODE)-[r]->(b:PNODE) ' \
          'WHERE a.nid = {nid1} ' + rel_str + \
          'RETURN DISTINCT b,' + inc_rel_str + 'ID(b)'

    params = {"nid1": nid1}
    if rel_type is not None:
        params['type'] = rel_type
    r = fire_cypher(cyp, params)

    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


def find_all_in_related_nodes(nid1, rel_type=None, include_relations=False):
    rel_str = "" if rel_type is None else "AND r.type = {type} "
    inc_rel_str = 'r,' if include_relations else ''
    cyp = 'MATCH (a:PNODE)<-[r]-(b:PNODE) ' \
          'WHERE a.nid = {nid1} ' + rel_str + \
          'RETURN DISTINCT b,' + inc_rel_str + 'ID(b)'

    params = {"nid1": nid1}
    if rel_type is not None:
        params['type'] = rel_type
    r = fire_cypher(cyp, params)

    if len(r.json()['errors']) > 0:
        return 1, r.json()
    else:
        return 0, r.json()


# [@PRODUCTIVITY MULTIPLIER]
# converts list type return data
# from the above methods to a flat readable list
def to_list(r):
    if r[0] == 1:
        # error, return as such
        return r
    else:
        finalList = []
        metaRowList = r[1]['results'][0]['data']
        for k in metaRowList:
            finalList.append(k['row'])
        return 0, finalList
