import matplotlib.pyplot as plt
import networkx as nx
from src.graph_builder import build_graph
from src.extractor import extract_triples
from src.utils import load_corpus

corpus = load_corpus("data/corpus.txt")
triples = extract_triples(corpus)
G = build_graph(triples)

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000)
edge_labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.savefig("outputs/graph.png")
plt.show()