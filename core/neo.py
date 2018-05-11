from neo4j.v1 import GraphDatabase

# password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver('bolt://192.168.1.118')

class GraphDb:
    def init(self):
        self.sess = diver.session()

    def insert_test(self):
        cyp = 'CREATE (p:Person {name:{name},born:{born}}) ' \
            'RETURN p, ID(p)'
        params = {"name": "Clint Eastwood", "born": 1930}
        r = self.sess.run(cyp, params)

        print(r.json())