import pandas as pd
import numpy as np
import os, sys

def open_json(path):
    f = open(path, 'r')
    df = pd.read_json(f)
    return df

def data_cleaning(path):
    df = open_json(path)

    domain_list = list()
    index_list = list()
    for idx, row in df.iterrows():
        unit = row["ThroughputSize"].split(" ")[1]
        df.loc[idx, "ThroughputSize"] = int(row["ThroughputSize"].split(" ")[0])
        if unit == "MB":
            df.loc[idx, "ThroughputSize"] = int(row["ThroughputSize"].split(" ")[0]) * (1024*1024)
        elif unit == "KB":
            df.loc[idx, "ThroughputSize"] = int(row["ThroughputSize"].split(" ")[0]) * 1024
        else:
            pass

        if row["Domain"] not in domain_list:
            domain_list.append(row["Domain"])
            index_list.append(idx)
            continue
        index = index_list[domain_list.index(row["Domain"])]
        df.loc[index, ["Throughput"]] = df.loc[index, ["Throughput"]] + row["Throughput"]
        
    df = df.drop_duplicates(subset=["Domain"], keep="first")
    df = df.reset_index()
    df.to_json(path)

def construct_one(path):
    data_cleaning(path)

    df = open_json(path)

    A = np.zeros((len(df), len(df)), dtype=np.int)
    X = np.zeros((len(df), 2), dtype=np.int)
    for idx, row in df.iterrows():
        edge = (df["ASN"] == row["ASN"])
        A[idx, :] = edge.astype(np.int)
        X[idx][0] = row["Throughput"]
        X[idx][1] = row["ThroughputSize"]

    np.savez(os.path.join("graph", "graph_focus", df["urlscan_uuid"][0] + ".npz"), A=A, X=X)
    return

def construct_all():
    files = os.listdir("json")
    for idx, file in enumerate(files):
        print("\r{}/{}, {}".format(idx+1, len(files), file), end="")
        construct_one(os.path.join("json", file))
    
    return

def main():
    if "graph" not in os.listdir("."):
        os.makedirs("graph")
    if "graph_focus" not in os.listdir("graph"):
        os.makedirs(os.path.join("graph", "graph_focus"))
    construct_all()

if __name__ == "__main__":
    main()
    # path = os.path.join("json", "794e9d63-6be6-4379-a3e0-c6b17dae5c38.json")
    # construct_one(path)

# DataFrame column / type
# AS <class 'str'>
# ASN <class 'numpy.int64'>
# IP <class 'str'>
# Label <class 'numpy.int64'>
# Throughput <class 'numpy.int64'>
# urlscan_uuid <class 'str'>

## usage python3 graph_focus.py