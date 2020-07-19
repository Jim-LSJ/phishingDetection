import os, sys
import pandas as pd

def read_data(path):
    data = pd.DataFrame(columns=["url"])

    idx = 0

    f = open(path, "r")
    while True:
        url = f.readline()
        if not url:
            break
        data.loc[idx, "url"] = url
        idx += 1

    return data

def label_overlap():
    # OP = pd.read_csv(os.path.join(sys.argv[1], "OpenPhish", "new_feed.txt"), delimiter="\n")
    # PT = pd.read_csv(os.path.join(sys.argv[1], "PhishTank", "new_url.txt"), delimiter="\n")
    OP = read_data(os.path.join(sys.argv[1], "OpenPhish", "new_feed.txt"))
    PT = read_data(os.path.join(sys.argv[1], "PhishTank", "new_url.txt"))

    idx = 0
    overlap = pd.DataFrame(columns=["url"])
    for url in PT["url"]:
        if url in OP["url"].tolist():
            overlap.loc[idx, "url"]= url
            idx += 1
    
    print(overlap)
    overlap.to_csv(os.path.join(sys.argv[1], "overlap_url.txt"), index=False)

if __name__ == "__main__":
    # if sys.argv[1] == "label":
    #     label_validation()
    label_overlap()

## Usage: python3 code/overlap.py <URL/20200712>