"""
Nodes: `n1`, `n2`, `n3`, `n4`, `n5`

(`n`s are people, who met each other at social events a different number of times)

SE1: n1, n2, n3
SE2: n1, n2, n3
SE3: n1, n4, n5
SE4: n1, n2, n3, n4 
SE4: n1, n2, n3, n4
"""


import community as community_louvain # pip install python-louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx

random_state = 2022

# create graph object
G = nx.Graph()

nodes = ["n1", "n2", "n3", "n4", "n5"]
for n in nodes:
    G.add_node(n, label=n)

"""
SE1: n1, n2, n3
SE2: n1, n2, n3
SE3: n1, n4, n5
SE4: n1, n4, n5
SE5: n2, n3
SE6: n4, n5

"""
# SE1: n1, n2, n3
G.add_edge("n1", "n2", weight=1)
G.add_edge("n1", "n3", weight=1)
G.add_edge("n2", "n3", weight=1)
# SE1+SE2: n1, n2, n3
G.add_edge("n1", "n2", weight=2)
G.add_edge("n1", "n3", weight=2)
G.add_edge("n2", "n3", weight=2)
#SE3: n1, n4, n5
G.add_edge("n1", "n4", weight=1)
G.add_edge("n1", "n5", weight=1)
G.add_edge("n4", "n5", weight=1)
#SE3+SE4: n1, n4, n5
G.add_edge("n1", "n4", weight=2)
G.add_edge("n1", "n5", weight=2)
G.add_edge("n4", "n5", weight=2)
#SE5: n2, n3
G.add_edge("n2", "n3", weight=3)
#SE5: n4, n5
G.add_edge("n4", "n5", weight=3)

"""
Tabular representation
n1	n2	2
n1	n3	2
n1	n4	2
n1	n5	2
n2	n3	3
n2	n4	0
n2	n5	0
n3	n4	0
n3	n5	0
n4	n5	3

Matrix representation
0	n1	n2	n3	n4	n5
n1	0	2	2	2	2	
n2	2	0	3	0	0
n3	2	3	0	0	0
n4	2	0	0	0	3
n5	2	0	0	3	0
"""


# generating graph viz
edges = G.edges()
weights = [G[u][v]['weight'] for u,v in edges]

pos = nx.spring_layout(G, seed=random_state)
nx.draw_networkx_nodes(G, pos, node_size=40, node_color="yellow")
nx.draw_networkx_edges(G, pos, alpha=0.5, width=weights)
nx.draw_networkx_labels(G, pos, font_size=10)

plt.show()

# metrics
#degree_centrality = nx.degree_centrality(G)
#closeness_centrality = nx.closeness_centrality(G)
#betweenness_centrality = nx.betweenness_centrality(G)
