import community as community_louvain # pip install python-louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx

random_state = 2022

# helper function to load data in from file
def get_data(filename):
    # use a context manager to load in the data
    with open(filename, 'r', encoding='utf8') as rf:
        # transform file into string and split along new line
        lines = rf.read().split("\n")

        # separate each line along the tab characters
        data = [line.split("\t") for line in lines]

        # grab the header
        header = data[0]

        # delete header from data
        data = data[1:]
    
    # return header and data
    return header, data

# load data in from file
node_header, node_data = get_data('sw_network_nodes_allCharacters.csv')
edge_header, edge_data = get_data('sw_network_edges_allCharacters.csv')

# create graph object
G = nx.Graph()

episode = "episode-5"
episodeNodes = []

# add edge information to the graph
for edge in edge_data:
    # add edge one by one, node 1, node 2, weight
    if episode in edge[3]:
        episodeNodes.append(edge[0])
        episodeNodes.append(edge[1])
        G.add_edge(edge[0], edge[1], weight=int(edge[2]))

# add node information to the graph
for node in node_data:
    if node[0] in episodeNodes:
        # add nodes one by one, with id, label, affiliation, and side
        G.add_node(node[0], label=node[1], affiliation=node[2], side=node[3])


# metrics
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

# visualize this
#nx.draw_spring(G)
#plt.show()

#G = nx.karate_club_graph()

#first compute the best partition
partition = community_louvain.best_partition(G)

# draw the graph
pos = nx.spring_layout(G, seed=random_state) # layout is always a bit random, hence we use `seed`
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=10)
plt.show()