import pandas as pd
import os, sys

def merge_benign():
    CC = pd.read_csv(os.path.join(sys.argv[1], "uuid.txt"))

    for i in range(len(CC)):
        CC.loc[i, "label"] = 0
        CC.loc[i, "source"] = "CC"

    CC.to_csv(os.path.join(sys.argv[1], "feature.csv"), index=False)

    return

def merge_phishing():
    assert ("feature.csv" not in os.listdir(sys.argv[1]) )   # avoid overwrite new data
    
    OP = pd.read_csv(os.path.join(sys.argv[1], "OpenPhish", "uuid.txt"))
    PT = pd.read_csv(os.path.join(sys.argv[1], "PhishTank", "uuid.txt"))

    for i in range(len(OP)):
        OP.loc[i, "label"] = 1
        OP.loc[i, "source"] = "OP"

    for i in range(len(PT)):
        PT.loc[i, "label"] = 1
        PT.loc[i, "source"] = "PT"


    out = pd.concat([OP, PT], axis=0, sort=False)
    out.to_csv(os.path.join(sys.argv[1], "feature.csv"), index=False)

    return

def merge_all():
    origin_data = pd.read_csv(os.path.join("URL","feature.csv"))
    new_data = pd.read_csv(os.path.join(sys.argv[1], "feature.csv"))

    for i in range(len(new_data)):
        new_data.loc[i, "graph_folder"] = sys.argv[1].split("/")[1]

    out = pd.concat([origin_data, new_data], axis=0, sort=False)
    out.to_csv(os.path.join("URL", "feature.csv"), index=False)

    return

if __name__=="__main__":
    # merge()
    if sys.argv[2] == "all":
        merge_all()
        print("Finish merge features")
    elif sys.argv[2] == "benign":
        merge_benign()
        print("Finish merge benign uuid")
    else:
        merge_phishing()
        print("Finish merge phishing uuid")
    

## Usage: python3 code/merge.py <URL/20200710> all
## Usage: python3 code/merge.py <URL/CommonCrawl_0> benign
## Usage: python3 code/merge.py <URL/CommonCrawl_0> others