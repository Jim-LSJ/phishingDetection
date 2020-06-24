import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os, sys

def open_json(path):
    f = open(path, 'r')
    df = pd.read_json(f)    
    return df

def visualize_graph_focus():
    path = os.listdir("graph/graph_focus")[17]
    A = np.load(os.path.join("graph", "graph_focus", path))["A"]
    G = nx.from_numpy_matrix(A)

    f = open(os.path.join("json", path.split(".")[0] + ".json"), 'r')
    df = pd.read_json(f)
    df["ASN"]
    attrs = dict()
    for i in range(len(df)):
        attrs[i] = {"ASN":df["ASN"][i]}
    nx.set_node_attributes(G, attrs)
    labels = nx.get_node_attributes(G, "ASN")
    # print(G.nodes)


    nx.draw(G, labels=labels)
    plt.show()

def visualize_node_focus():
    A = np.load(os.path.join("graph", "node_focus", "node_focus_ASN.npz"))["A"]

    domain_list = list()
    label_list = list()
    files = os.listdir("json")
    for idx, file in enumerate(files):
        if idx >= 100:
            break

        print("\r{}/{}, {}".format(idx+1, len(files), file), end="")
        df = open_json(os.path.join("json", file))
        domain_list.append(df["Domain"][0])
        label_list.append(df["Label"][0])

    _A = np.zeros((100, 100), dtype=np.int)
    for i in range(100):
        _A[i] = A[i][:100]
    
    print(_A)
    print(len(_A), len(_A[0]))

    G = nx.from_numpy_matrix(_A)

    attrs = dict()
    for i in range(len(domain_list)):
        attrs[i] = {"Domain":domain_list[i]}
    nx.set_node_attributes(G, attrs)
    labels = nx.get_node_attributes(G, "Domain")
    
    nx.draw(G, node_color=label_list)
    plt.show()

visualize_node_focus()