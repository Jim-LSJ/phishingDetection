import os, sys
import pandas as pd

def label_validation():
    OP = pd.read_csv(os.path.join("URL", "OpenPhish", "feed.txt"), delimiter="\n")
    PT = pd.read_csv(os.path.join("URL", "PhishTank", "url.txt"))

    idx = 0
    overlap = pd.DataFrame(columns=["url"])
    for url in PT["url"]:
        if url in OP["url"].tolist():
            overlap.loc[idx, "url"]= url
            idx += 1
    
    print(overlap)
    overlap.to_csv(os.path.join("URL", "overlap_url.txt"), index=False)

if __name__ == "__main__":
    # if sys.argv[1] == "label":
    #     label_validation()
    label_validation()