import pandas as pd
import os, sys

# def merge():
#     OP = pd.read_csv(os.path.join("URL", "OpenPhish", "uuid_graph.csv"))
#     PT = pd.read_csv(os.path.join("URL", "PhishTank", "uuid_graph.csv"))
#     CC = pd.read_csv(os.path.join("URL", "CommonCrawl", "uuid_graph.csv"))

#     for i in range(len(OP)):
#         OP.loc[i, "label"] = 1
#         OP.loc[i, "source"] = "OP"

#     for i in range(len(PT)):
#         PT.loc[i, "label"] = 1
#         PT.loc[i, "source"] = "PT"

#     for i in range(len(CC)):
#         CC.loc[i, "label"] = 0
#         CC.loc[i, "source"] = "CC"

#     out = pd.concat([OP, PT, CC], axis=0, sort=False)
#     out.to_csv(os.path.join("URL", "uuid_graph.csv"), index=False)

#     return

def merge_phishing():
    assert ("uuid_graph.csv" not in os.listdir(sys.argv[1]) )   # avoid overwrite new data
    
    OP = pd.read_csv(os.path.join(sys.argv[1], "OpenPhish", "uuid.txt"))
    PT = pd.read_csv(os.path.join(sys.argv[1], "PhishTank", "uuid.txt"))

    for i in range(len(OP)):
        OP.loc[i, "label"] = 1
        OP.loc[i, "source"] = "OP"

    for i in range(len(PT)):
        PT.loc[i, "label"] = 1
        PT.loc[i, "source"] = "PT"


    out = pd.concat([OP, PT], axis=0, sort=False)
    out.to_csv(os.path.join(sys.argv[1], "uuid_graph.csv"), index=False)

    return

def merge_all():
    origin_data = pd.read_csv(os.path.join("URL","uuid_graph.csv"))
    new_data = pd.read_csv(os.path.join(sys.argv[1], "uuid_graph.csv"))

    out = pd.concat([origin_data, new_data], axis=0, sort=False)
    out.to_csv(os.path.join("URL", "uuid_graph.csv"), index=False)

    return

if __name__=="__main__":
    # merge()
    if sys.argv[2] == "all":
        merge_all()
        print("Finish merge features")
    else:
        merge_phishing()
        print("Finish merge uuid")
    

## Usage: python3 code/merge.py <URL/20200710>