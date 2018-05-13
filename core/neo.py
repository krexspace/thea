from neo4j.v1 import GraphDatabase
"""
refer: https://neo4j.com/docs/api/python-driver/current/
"""
# password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver('bolt://192.168.1.118')

class GraphDb:
    def __init__(self):
        self.sess = driver.session()

    def fire_cypher_single(self, cyp, params):
        r = self.sess.run(cyp, params)
        rec = r.single()
        if rec is None:
            raise Exception("Unexpected result None.")
        dic = {}
        for kv in rec[0].items():
            dic[kv[0]] = kv[1]
        return dic

    def fire_cypher_multi(self, cyp, params):
        r = self.sess.run(cyp, params)
        resp = []
        for rec in r:
            dic = {}
            for rec_vals in rec.values():
                if type(rec_vals) is int:
                    dic['id'] = rec_vals # id is expected when type is int
                else:
                    for kv in rec_vals.items():
                        dic[kv[0]] = kv[1]
            resp.append(dic)
        return resp

    def fire_cypher_empty(self, cyp, params):
        r = self.sess.run(cyp, params)
        return None

    # from neo.base import insert_test_1 as in1
    def insert_test_1(self):
        cyp = 'CREATE (p:Person {name:{name},born:{born}}) ' \
            'RETURN p, ID(p)'
        params = {"name": "Clint Eastwood", "born": 1930}
        r = self.fire_cypher_single(cyp, params)
        return r

    # from neo.base import insert_node as ins
    def insert_node_nid(self, nid):
        cyp = 'CREATE (p:PNODE {nid:{nid}}) RETURN p, ID(p)'
        params = {"nid": nid}
        r = self.fire_cypher_single(cyp, params)
        return r


    # Same as below but expects a dictionary
    def insert_node(self, args):
        if 'nid' not in args:
            raise  Exception("nid is required to create a node")
        # build param string
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
        r = self.fire_cypher_single(cyp, params)
        return r


    # nb.insert_node(nid='TEST02', title='Cool days', url='http://cool.domain/island')
    def insert_node2(self, **args):
        return insert_node(args)


    # from neo.base import insert_rel_by_id as inr
    # Here id is the Nodes' native neo ID
    def insert_rel_by_id(self, id1, id2, st):
        cyp = 'MATCH (a:PNODE),(b:PNODE) ' \
            'WHERE ID(a) = {id1} AND ID(b) = {id2} ' \
            'CREATE (a)-[r:NCONN {st:{st}}]->(b) ' \
            'RETURN r, ID(r)'

        params = {"id1": id1, "id2": id2, "st": st}
        r = self.fire_cypher_single(cyp, params)
        return r


    # from neo.base import insert_rel_by_nid as inr
    # dir 1 is outgoing, 2 is incoming
    def insert_rel_by_nid(self, nid1, nid2, st=50, rel_type="STD", direction=1):
        if direction == 0:
            raise Exception("Bi-directional relationships are not supported")
        elif direction == 1:
            # out going: nid1 -> nid2
            rel_str = '(a)-[r:NCONN {st:{st},type:{type}}]->(b) '
        elif direction == 2:
            # in coming: nid1 <- nid2
            rel_str = '(a)<-[r:NCONN {st:{st},type:{type}}]-(b) '
        else:
            raise Exception("Invalid direction")

        cyp = 'MATCH (a:PNODE),(b:PNODE) ' \
            'WHERE a.nid = {nid1} AND b.nid = {nid2} ' \
            'CREATE ' + rel_str +\
            'RETURN r, ID(r)'

        params = {"nid1": nid1, "nid2": nid2, "st": st, "type": rel_type}
        r = self.fire_cypher_single(cyp, params)
        # returns the new rel id
        return r


    def delete_rel_by_nid(self, nid1, nid2, rel_type="STD"):
        if rel_type is not None:
            type_str = 'AND r.type = {type} '
        else:
            type_str = ''
        cyp = 'MATCH (a:PNODE)-[r:NCONN]-(b:PNODE) ' \
            'WHERE a.nid = {nid1} AND b.nid = {nid2} ' + type_str +\
            'DELETE r'
        
        params = {"nid1": nid1, "nid2": nid2, "type": rel_type}
        r = self.fire_cypher_empty(cyp, params)
        # returns the new rel id
        return r

    # Delete a relationship by its native neo ID
    def delete_rel_by_relid(self, rel_id):
        cyp = 'MATCH ()-[r:NCONN]-() ' \
            'WHERE ID(r) = {rel_id} ' \
            'DELETE r'

        params = {"rel_id": rel_id}
        r = self.fire_cypher_empty(cyp, params)
        # returns the new rel id
        return r

    # deletes all irrespective of relation type
    def delete_all_rel_by_nid(self, nid1, nid2):

        cyp = 'MATCH (a:PNODE)-[r:NCONN]-(b:PNODE) ' \
            'WHERE a.nid = {nid1} AND b.nid = {nid2} ' \
            'DELETE r'

        params = {"nid1": nid1, "nid2": nid2}
        r = self.fire_cypher_empty(cyp, params)
        # returns the new rel id
        return r

    # from neo.base import delete_all as del_all
    def delete_all(self):
        cyp = 'MATCH (a) DETACH DELETE a'
        params = None
        r = self.fire_cypher_empty(cyp, params)
        return r


    # delete by nid
    def delete_by_nid(self, nid):
        cyp = 'MATCH (a:PNODE) WHERE a.nid = {nid} DETACH DELETE a'
        params = {"nid": nid}
        r = self.fire_cypher_empty(cyp, params)
        return r

    # Usage
    def select_by_nid(self, nid):
        cyp = 'MATCH (a:PNODE) WHERE a.nid = {nid} RETURN a'
        params = {"nid": nid}
        r = self.fire_cypher_single(cyp, params)
        return r

    # Usage
    def select_all(self, limit=100):
        cyp = 'MATCH (a) RETURN a LIMIT {limit}'
        params = {"limit": limit}
        r = self.fire_cypher_multi(cyp, params)
        return r


    # rel type and strenth has to be passed or will be reset 
    # # to defaults
    def update_rel_by_relid(self, rel_id, st=50, rel_type="STD", ):
        cyp = 'MATCH ()-[r:NCONN]-() ' \
            'WHERE ID(r) = {rel_id} ' \
            'SET r.st = {st}, r.type = {rel_type}'

        params = {"rel_id": rel_id, "rel_type": rel_type, "st": st}
        r = self.fire_cypher_multi(cyp, params)
        # returns the new rel id
        return r

    def find_all_relations(self, nid1, nid2, rel_type=None):
        rel_str = "" if rel_type is None else "AND r.type = {type} "
        cyp = 'MATCH (a:PNODE)-[r]-(b:PNODE) ' \
            'WHERE a.nid = {nid1} AND b.nid = {nid2} ' + rel_str +\
            'RETURN r, ID(r)'

        params = {"nid1": nid1, "nid2": nid2}
        if rel_type is not None:
            params['type'] = rel_type
        r = self.fire_cypher_multi(cyp, params)
        return r


    def find_all_out_relations(self, nid1, nid2, rel_type=None):
        rel_str = "" if rel_type is None else "AND r.type = {type} "
        cyp = 'MATCH (a:PNODE)-[r]->(b:PNODE) ' \
            'WHERE a.nid = {nid1} AND b.nid = {nid2} ' + rel_str + \
            'RETURN r, ID(r)'

        params = {"nid1": nid1, "nid2": nid2}
        if rel_type is not None:
            params['type'] = rel_type
        r = self.fire_cypher_multi(cyp, params)
        return r


    def find_all_in_relations(self, nid1, nid2, rel_type=None):
        rel_str = "" if rel_type is None else "AND r.type = {type} "
        cyp = 'MATCH (a:PNODE)<-[r]-(b:PNODE) ' \
            'WHERE a.nid = {nid1} AND b.nid = {nid2} ' + rel_str + \
            'RETURN r, ID(r)'

        params = {"nid1": nid1, "nid2": nid2}
        if rel_type is not None:
            params['type'] = rel_type
        r = self.fire_cypher_multi(cyp, params)
        return r


    def find_all_related_nodes(self, nid1, rel_type=None, include_relations=False):
        rel_str = "" if rel_type is None else "AND r.type = {type} "
        inc_rel_str = 'r,' if include_relations else ''
        cyp = 'MATCH (a:PNODE)-[r]-(b:PNODE) ' \
            'WHERE a.nid = {nid1} ' + rel_str + \
            'RETURN DISTINCT b,' + inc_rel_str + 'ID(b)'

        params = {"nid1": nid1}
        if rel_type is not None:
            params['type'] = rel_type
        r = self.fire_cypher_multi(cyp, params)
        return r


    def find_all_out_related_nodes(self, nid1, rel_type=None, include_relations=False):
        rel_str = "" if rel_type is None else "AND r.type = {type} "
        inc_rel_str = 'r,ID(r),' if include_relations else ''
        cyp = 'MATCH (a:PNODE)-[r]->(b:PNODE) ' \
            'WHERE a.nid = {nid1} ' + rel_str + \
            'RETURN DISTINCT b,' + inc_rel_str + 'ID(b)'

        params = {"nid1": nid1}
        if rel_type is not None:
            params['type'] = rel_type
        r = self.fire_cypher_multi(cyp, params)
        return r


    def find_all_in_related_nodes(self, nid1, rel_type=None, include_relations=False):
        rel_str = "" if rel_type is None else "AND r.type = {type} "
        inc_rel_str = 'r,' if include_relations else ''
        cyp = 'MATCH (a:PNODE)<-[r]-(b:PNODE) ' \
            'WHERE a.nid = {nid1} ' + rel_str + \
            'RETURN DISTINCT b,' + inc_rel_str + 'ID(b)'

        params = {"nid1": nid1}
        if rel_type is not None:
            params['type'] = rel_type
        r = self.fire_cypher_multi(cyp, params)
        return r

'''
# Basic Test
g = GraphDb()
g.connect()
r = g.insert_test_1()
print(r.single())
'''