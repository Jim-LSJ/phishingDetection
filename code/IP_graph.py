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

def parse_one_dom(date, uuid):
    # parse urlscan/date/uuid/result_page.html
    # return a dict() containing ip, asn, as, domain, main_ip, throughput between ips, thoughput size
    
    df = pd.DataFrame()

    file = open(os.path.join("urlscan", date, uuid, "result_page.html"), "r")
    soup = BeautifulSoup(file.read(), "html.parser")
    file.close()

    ipdetail = soup.find("div", {"id": "ipdetail"})
    if not ipdetail:
        return

    label = soup.find(class_="panel-body").find("h4").find(class_="red")
    label = 1 if label else 0

    screenshots = ipdetail.find_all(class_="screenshot")
    for s in screenshots:
        throughput = s.find("b").text
        ip = s.find("tt").text
        ASN = s.find("small").find_previous_sibling("a").text.replace("ASN", "")
        AS = s.find("small").find("a").text
        Domain = ".".join(s.find(class_="condensed").find("a").text.split(".")[-2:])
        # throughput_size = soup.find(id="regdomaindetail").find("a", href=re.compile("/domain/(.)*" + Domain.replace(".", "\.")))
        # if throughput_size:
        #     throughput_size = throughput_size.parent.find_next_sibling("td").text
        # else:
        #     throughput_size = "x"
        #     print(Domain)
        
        df = df.append({"urlscan_uuid": uuid,
                        "Throughput": throughput,
                        "IP": ip,
                        "ASN": ASN,
                        "AS": AS,
                        "Domain": Domain,
                        # "ThroughputSize": throughput_size,
                        "label": label
                        }, ignore_index=True)

    df.to_json(os.path.join("json", uuid + ".json"))

    pass

def parse_all_dom():
    # pd.read_csv(URL/feature.csv)
    # for loop to call date
    #   for loop to call parse_one_dom(date, uuid) and construct a pd.DataFrame
    # store the uuid and dict() to a csv
    pass

def construct_graph():
    # read the result csv
    # read feature.csv
    # get unique ip
    # contruct A with by edge1(main_ip to src_ip) and edge2(ip with same asn)
    # store A to npy

    # construct X with asn, top 8 bits ip, feature by mapping uuid to feature.csv
    # store X to npy
    
    # construct y and train_mask, val_mask, test_mask
    # store y, train_mask, val_mask, test_mask to npz
    pass

def main():
    parse_one_dom("20200710", "0a00a681-9ab3-4d1f-9d6c-cad8d02014cd")

if __name__ == "__main__":
    main()