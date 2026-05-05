import networkx as nx


def normalize(x):
    return x.strip().lower()


def build_graph(triples):
    G = nx.Graph()

    for s, r, o in triples:
        s = normalize(s)
        o = normalize(o)
        relation = r.strip().upper().replace(" ", "_")
        
        G.add_node(s)
        G.add_node(o)
        G.add_edge(s, o, relation=r)

    return G