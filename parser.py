from bs4 import BeautifulSoup
import json, sys, os, re
import pandas as pd

def parse_one(uuid):
    df = pd.DataFrame()

    file = open(os.path.join("urlscan", uuid, "result_page.html"), "r")
    html = file.read()
    soup = BeautifulSoup(html, "html.parser")
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
        throughput_size = soup.find(id="regdomaindetail").find("a", href=re.compile("/domain/(.)*" + Domain.replace(".", "\.")))
        if throughput_size:
            throughput_size = throughput_size.parent.find_next_sibling("td").text
        else:
            throughput_size = "x"
            print(Domain)
        
        df = df.append({"urlscan_uuid": uuid,
                        "Throughput": throughput,
                        "IP": ip,
                        "ASN": ASN,
                        "AS": AS,
                        "Domain": Domain,
                        "ThroughputSize": throughput_size,
                        "Label": label
                        }, ignore_index=True)

    df.to_json(os.path.join("json", uuid + ".json"))

    return

    # ipsummary = soup.find("div", {"id": "ipsummary"})

    # if not ipsummary: # nonetype because of no scanning result
    #     return

    # tr = ipsummary.find("tbody").find_all("tr")
    # for row in tr:
    #     if len(row.attrs) and row.attrs["class"][0] == "summary":
    #         continue
    #     td = row.find_all("td")
    #     throughput = td[0].find("b").text
    #     ip = td[1].find("span", class_="hidden-xs").text
    #     flag = td[2]
    #     ASN = td[3].find("a").text
    #     AS = td[3].find("small", class_="hidden-xs").text
    #     df = df.append({"urlscan_uuid": uuid,
    #                     "Throughput": throughput,
    #                     "IP": ip,
    #                     "ASN": ASN,
    #                     "AS": AS,
    #                     "Label": label
    #                     }, ignore_index=True)

def parse_all(uuids):
    for idx, uuid in enumerate(uuids.values):
        #####################
        # control
        #####################
        # if idx <= 1672:
        #     continue
        # if idx > 1673:
        #     break
        #####################

        print("\r{}/{}, {}".format(idx+1, len(uuids), uuid), end="")
        parse_one(uuid)

    print()

    return

def main():
    if "json" not in os.listdir("."):
        os.makedirs("json")
    uuidFile = pd.read_csv(sys.argv[1])
    uuids = uuidFile["UUID"]
    parse_all(uuids)

if __name__ == "__main__":
    # main()
    uuid = os.path.join("794e9d63-6be6-4379-a3e0-c6b17dae5c38")
    parse_one(uuid)


## usage example: python3 parser.py 20200511.csv