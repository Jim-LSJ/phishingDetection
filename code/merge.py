import pandas as pd
import os, sys

def merge():
    OP = pd.read_csv(os.path.join("URL", "OpenPhish", "uuid_graph.csv"))
    PT = pd.read_csv(os.path.join("URL", "PhishTank", "uuid_graph.csv"))
    CC = pd.read_csv(os.path.join("URL", "CommonCrawl", "uuid_graph.csv"))

    for i in range(len(OP)):
        OP.loc[i, "label"] = 1
        OP.loc[i, "source"] = "OP"

    for i in range(len(PT)):
        PT.loc[i, "label"] = 1
        PT.loc[i, "source"] = "PT"

    for i in range(len(CC)):
        CC.loc[i, "label"] = 0
        CC.loc[i, "source"] = "CC"

    out = pd.concat([OP, PT, CC], axis=0, sort=False)
    out.to_csv(os.path.join("URL", "uuid_graph.csv"), index=False)

    return

if __name__=="__main__":
    merge()

## Usage: python3 merge.py