import os, sys
import bs4
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# Node Focus
# Node: domain IP (contain main ip and src ip)
# Edge: two types
#       1. main ip bidirected to src ip
#       2. IP with same ASN
# Node property: asn, top 8 or 16 bits IP, main ip can have features in feature.csv (src ip feature = 0)

# a TOTAL_IP_LIST consist of all distinct ips
# In TOTAL_IP_LIST, {ip: {
#                       "first_ip": top 8 bits of ip
#                       "ASN": asn, "features in feature.csv": feature if ip is url_main_ip, else 0
#                       other feature of ip obtained by urlscan in the future will do
#                       }}

def parse_one_dom(date, uuid, df):
    file = open(os.path.join("urlscan", date, uuid, "result_page.html"), "r")
    soup = BeautifulSoup(file.read(), "html.parser")
    file.close()

    # no result page
    main = soup.find(class_="main")
    if not main.h1.find("small"):
        return df

    if main.find("h2", class_="text-danger"):
        if  main.find("h2", class_="text-danger").text == "We could not scan this website!":
            return df

    main_ip = main.h1.find("small").text[:-1]

    ipdetail = soup.find("div", {"id": "ipdetail"})
    if not ipdetail:
        return df

    screenshots = ipdetail.find_all(class_="screenshot")
    for s in screenshots:
        throughput = s.find("b").text
        ip = s.find("tt").text
        ASN = s.find("small").find_previous_sibling("a").text.replace("ASN", "")
        AS = s.find("small").find("a").text
        Domain = ".".join(s.find(class_="condensed").find("a").text.split(".")[-2:])
        
        is_main_ip = (ip == main_ip)

        df = df.append({"urlscan_uuid": uuid,
                        "Throughput": throughput,
                        "IP": ip,
                        "ASN": ASN,
                        "AS": AS,
                        "Domain": Domain,
                        "is_main_ip": is_main_ip
                        }, ignore_index=True)

    return df

def parse_all_dom():
    feature = pd.read_csv("URL/feature_preprocessed.csv")
    df = pd.DataFrame()

    for idx in range(len(feature)):
        # if idx <= 24000:
        #     continue
        print("\r{}/{}".format(idx, len(feature)), end="")
        df = parse_one_dom(feature.loc[idx, "graph_folder"], feature.loc[idx, "UUID"], df)

        if idx % 1000 == 0:
            df = df.dropna()
            df.to_csv("IP_graph_data.csv", index=False)

    df = df.dropna()
    df.to_csv("IP_graph_data.csv", index=False)
    print("\nFinish IP parse")

def construct_graph():
    feature = pd.read_csv("URL/feature_preprocessed.csv")
    ip_df = pd.read_csv("IP_graph_data.csv")

    main_ip = ip_df[ip_df["is_main_ip"] == 1]
    src_ip = ip_df[ip_df["is_main_ip"] == 0]
    unique_main_ip = main_ip.drop_duplicates("IP")
    unique_src_ip = src_ip.drop_duplicates("IP")

    feature_col = ['div', 'img', 'iframe', 'a', 
                    'script', 'external_script', 'internal_script', 
                    'form', 'input', 'textarea', 'sensitive',
                    'Tags', 'No-class Tags', 'class Tags',
                    'Cookies', 'secure', 'session', 'httponly', 'Rule',
                    'JSGlobalVar', 'Requests', 'Ad-blocked',
                    'HTTPS', 'IPv6', 'Domains', 'Subdomains', 'IPs',
                    'Countries', 'Transfer', 'Size', 'OutGoingLinks'
                    ]

    NODE_NUM = len(main_ip) + len(unique_src_ip)
    print(len(main_ip), len(unique_src_ip), NODE_NUM)
    FEATURE_NUM = len(feature_col)
    A = np.zeros((NODE_NUM, NODE_NUM), dtype=bool)
    X = np.zeros((NODE_NUM, FEATURE_NUM + 1), dtype=np.int)
    y = np.zeros((NODE_NUM, 3), dtype=int)  # one hot encoding, 0: benign, 1: phishing, 2: src ip
    
    # construct Edge1 main ip and src ip relationship
    idx, main_idx, label_idx = 0, 0, 0
    unique_src = dict()
    for i in range(len(ip_df)):
        print("\ri: {}, idx: {}, main_idx: {}, ASN: {}".format(i, idx, main_idx, ip_df.loc[i, "ASN"]), end="")
        if ip_df.loc[i, "is_main_ip"] == 1:
            main_idx = idx
            X[idx, : FEATURE_NUM] = feature.loc[label_idx, feature_col].to_numpy()
            X[idx, -1] = int(ip_df.loc[i, "ASN"])
            # X[idx, : -1] = int(ip_df.loc[i, "IP"].split(".")[0]) 
            y[idx, int(feature.loc[label_idx, "label"])] = 1
            label_idx += 1
            idx += 1
        else:
            # src_ip is existing
            if unique_src.get(ip_df.loc[i, "IP"]):
                A[unique_src.get(ip_df.loc[i, "IP"]), main_idx] = 1
                A[main_idx, unique_src.get(ip_df.loc[i, "IP"])] = 1
            # src ip is not existing
            else:
                unique_src[ip_df.loc[i, "IP"]] = idx    # append to dictionary
                A[idx, main_idx] = 1
                A[main_idx, idx] = 1
                X[idx, -1] = int(ip_df.loc[i, "ASN"])
                # X[idx, -1] = int(ip_df.loc[i, "IP"].split(".")[0]) 
                y[idx, 2] = 1   # label = 2 means src ip
                idx += 1
    
    
    asn_dict = dict()
    for i in range(len(X)):
        if asn_dict.get(X[i, -1]):
            asn_dict[X[i, -1]].append(i)
        else:
            asn_dict[X[i, -1]] = [i]

    _X = np.zeros((NODE_NUM, FEATURE_NUM + 1 + len(asn_dict)), dtype=np.int)
    idx = 0
    for key, value in asn_dict.items():
        for i in value:
            A[i, value] = 1
            A[i, i] = 0
            _X[i, FEATURE_NUM + 1 + idx] = 1
        idx += 1

    # try:
    #     os.makedirs(op.path.join("graph", "IP_graph"))
    # except:
    #     pass

    print(_X.shape)
    np.savez(os.path.join("graph", "IP_graph", "IP_graph.npz"), A=A, X=_X, y=y)
    
    # construct y and train_mask, val_mask, test_mask
    # store y, train_mask, val_mask, test_mask to npz
    pass

def main():
    # parse_all_dom()
    construct_graph()

if __name__ == "__main__":
    main()