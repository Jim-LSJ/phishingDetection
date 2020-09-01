import pandas as pd
import hashlib
import os, sys
from bs4 import BeautifulSoup

def sha1_hash(html):
    s = hashlib.sha1()  # initiate sha1 object before hash
    s.update(html.encode())
    h = s.hexdigest()
    return h

def main():
    # df = pd.read_csv("feature.csv")
    df = pd.read_csv(sys.argv[1])
    for i in range(len(df)):
        folder = df.loc[i, "folder"]
        uuid = df.loc[i, "UUID"]
        print("\r{}/{}, {}/{}".format(i, len(df), str(int(folder)), uuid), end="")

        if sys.argv[1][0] == "U":
            file = open(os.path.join("html", str(int(folder)), uuid + ".html"))
            outer = BeautifulSoup(file.read(), "html.parser")
            file.close()
            soup = outer
        else:
            file = open(os.path.join("urlscan", str(int(folder)), uuid, "dom_page.html"))
            outer = BeautifulSoup(file.read(), "html.parser")
            file.close()

            html = outer.pre.text
            soup = BeautifulSoup(html, "html.parser")

        for elem in soup.find_all("input"):
            elem["value"] = ""
            elem["placeholder"] = ""
            elem["area-label"] = ""

        html = soup.prettify()
        html = html.replace(" ", "")    # delete space
        html = html.replace("\n", "")    # delete end line
        html = html.replace("\t", "")    # delete tab

        hash_value = sha1_hash(html)
        df.loc[i, "hash_value"] = hash_value

    # df.to_csv("feature.csv", index=False)
    df.to_csv(sys.argv[1], index=False)
    print("\nEnd hash")

if __name__ == "__main__":
    main()

# Usage: python3 code/hash_near_duplicate.py feature.csv
# Usage: python3 code/hash_near_duplicate.py URL/20200826/feature.csv