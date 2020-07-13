import os, sys
import bs4
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt

NUM_OF_NODES = 1000
NODE_COUNTER = 0

def traverse(node, A, X, parent_node_idx, node_idx, property_list, depth, depth_list):
    global NODE_COUNTER
    # print(node.name, parent_node_idx, node_idx)
    
    if node_idx >= len(A):
        return

    for n in node.contents:
        if type(n) != bs4.element.Tag:
            continue
        
        NODE_COUNTER += 1
        traverse(n, A, X, node_idx, NODE_COUNTER, property_list, depth + 1, depth_list)

    # tag attribute
    for idx, _property in enumerate(property_list):
        if node.attrs.get(_property):
            X[node_idx][idx] = 1
    
    X[node_idx][-1] = len(node.text)    # text length

    if node_idx != 0:
        A[node_idx][parent_node_idx] = 1
    depth_list[depth].append(node_idx)

    return

def construct_one_dom(uuid = "8e441f5e-44de-4a59-a505-9990c927d628"):
    global NODE_COUNTER, NUM_OF_NODES
    path = os.path.join("urlscan", uuid, "dom_page.html")
    file = open(path)
    soup = BeautifulSoup(file.read(), "html.parser")
    file.close()
    
    if not soup.pre:
        return False

    page_dom = soup.pre.text
    soup = BeautifulSoup(page_dom, "html.parser")

    # NUM_OF_NODES = len(soup.find_all()) + 1
    
    f_p = open("Attributes.txt", "r").read()
    property_list = f_p.split('\n')[:-1]

    # A: Adjacency Matrix of DOM Tree
    A = np.zeros((NUM_OF_NODES, NUM_OF_NODES), dtype=np.int)
    
    # X: Node Property Matrix
    X = np.zeros((NUM_OF_NODES, len(property_list) + 1), dtype=np.int)
    
    depth_list = [[] for i in range(len(soup.find_all()) + 1)]
    
    traverse(soup, A, X, parent_node_idx=0, node_idx=NODE_COUNTER, property_list=property_list,
            depth=0, depth_list=depth_list)
    
    np.savez(os.path.join("graph", "DOM_tree_100", uuid + ".npz"), A=A, X=X)

    # print(A)
    # print(X)
    # visualize_graph_focus(A)
 
    return True

def construct_all():
    global NODE_COUNTER
    uuids = pd.read_csv(sys.argv[1]) # <URL/OpenPhish/uuid.txt>
    for idx, uuid in enumerate(uuids["UUID"]):
        print("\r{}/{}, {}".format(idx+1, len(uuids), uuid), end="")
        uuids.loc[idx, "Graph"] = construct_one_dom(uuid)
        NODE_COUNTER = 0

    uuids.to_csv(sys.argv[1].split('.')[0] + "_graph.csv", index=False)
    return

def visualize_graph_focus(A):
    G = nx.from_numpy_matrix(A, create_using=nx.DiGraph())
    nx.draw(G)
    plt.show()

def main():
    try:
        os.makedirs(os.path.join("graph", "DOM_tree"))
    except:
        pass
    construct_all()
    # construct_one_dom()

    print("\nFinish")

if __name__ == "__main__":
    main()

## Usage: python3 DOM_graph.py <URL/OpenPhish/uuid.txt>