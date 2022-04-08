# NB: built on <>

import community as community_louvain # pip install python-louvain
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import itertools, io
import pandas as pd

random_state = 2022

def generateTopicsNetwork(file):
    with open(file, "r", encoding="utf8") as f1:
        edgesModeled = ["source\ttarget\tweight"]
        # transform file into string and split along new line
        lines = f1.read().split("\n")

        # separate each line along the tab characters
        data = [line.split("\t") for line in lines]

        # grab the header
        header = data[0]

        # delete header from data
        data = data[1:]

        topics = {}
        probs = {}

        for d in data:
            if d[1] in topics:
                topics[d[1]].append(d[3])
            else:
                topics[d[1]] = []
                topics[d[1]].append(d[3])
            probs[d[3]+"_"+d[1]] = float(d[2])

        # generate combinations
        for k,v in topics.items():
            combs = list(itertools.combinations(v[:10], 2))
            #print(combs)
            for e in combs:
                e = sorted(list(e)) # this is important to ensure that we avoid duplicate edges like A->B and B->A (our data is undirected)
                #print(e)
                weight = (probs[e[0]+"_"+k] + probs[e[1]+"_"+k])/2
                e.append(str(weight))
                e = "\t".join(e)
                edgesModeled.append(e)
        
        print("\tSaving results...")
        edgesModeled = "\n".join(edgesModeled)

    with open("TM_network.tsv", "w", encoding="utf8") as f9:
        f9.write(edgesModeled)
    print("-"*50)

    # graph results
    scoresData = io.StringIO(edgesModeled)
    scoresData = pd.read_csv(scoresData, sep="\t", header=0)

generateTopicsNetwork("LDA_model__years_1860_1864_40topics_TIDY_for_SNA.tsv")


# helper function to load data in from file
def get_data(filename):
    # use a context manager to load in the data
    with open(filename, 'r', encoding='utf8') as rf:
        lines = rf.read().split("\n") # transform file into string and split along new line
        data = [line.split("\t") for line in lines] # separate each line along the tab characters
        header = data[0] # grab the header
        data = data[1:] # delete header from data
    
    # return header and data
    return header, data

# load data in from file
node_header, node_data = get_data('TM_network.tsv')
edge_header, edge_data = get_data('TM_network.tsv')

# create graph object
G = nx.Graph()

# add node information to the graph
for node in node_data:
    # add nodes one by one, from edges data
    G.add_node(node[0], name=node[0])
    G.add_node(node[1], name=node[1])

# add edge information to the graph
for edge in edge_data:
    # add edge one by one, node 1, node 2, weight
    G.add_edge(edge[0], edge[1], weight=float(edge[2]))

# metrics
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

partition = community_louvain.best_partition(G)

print(betweenness_centrality)

# draw the graph
plt.rcParams["figure.figsize"] = (20, 15)
pos = nx.spring_layout(G, seed=random_state) # layout is always a bit random, hence we use `seed`
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=20, cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=5)

plt.savefig("TopicNetwork.png", dpi=150)
plt.savefig("TopicNetwork.pdf", dpi=150)
#plt.show()


