import pandas as pd
import numpy as np
import os, sys

def open_json(path):
    f = open(path, 'r')
    df = pd.read_json(f)    
    return df

def construct():
    ip_dict = dict()
    files = os.listdir("json")
    for idx, file in enumerate(files):
        print("\r{}/{}, {}".format(idx+1, len(files), file), end="")
        df = open_json(os.path.join("json", file))
        
        for index, row in df.iterrows():
            if not ip_dict.get(row["IP"]):
                ip_dict[row["IP"]] = [idx]
            else:
                ip_dict[row["IP"]].append(idx)

    A = np.zeros((len(files), len(files)), dtype=np.int)
    for key, value in ip_dict.items():
        if len(value) > 1:
            print(value)
        for v1 in value:
            for v2 in value:
                A[v1, v2] = 1
    print("len(dict) = {}".format(len(ip_dict)))
    np.savez(os.path.join("graph", "node_focus", "node_focus_ip.npz"), A=A)
    return

def main():
    if "graph" not in os.listdir("."):
        os.makedirs("graph")
    if "node_focus" not in os.listdir("graph"):
        os.makedirs(os.path.join("graph", "node_focus"))
    construct()

if __name__ == "__main__":
    main()

# DataFrame column / type
# AS <class 'str'>
# ASN <class 'numpy.int64'>
# IP <class 'str'>
# Label <class 'numpy.int64'>
# Throughput <class 'numpy.int64'>
# urlscan_uuid <class 'str'>

## usage python3 node_focus.py