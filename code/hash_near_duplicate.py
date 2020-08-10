import pandas as pd
import hashlib
import os
from bs4 import BeautifulSoup

def sha1_hash(html):
    s = hashlib.sha1()  # initiate sha1 object before hash
    s.update(html.encode())
    h = s.hexdigest()
    return h

def main():
    df = pd.read_csv("url_unique.csv")
    for i in range(len(df)):
        folder = df.loc[i, "folder"]
        uuid = df.loc[i, "UUID"]
        print("\r{}/{}, {}/{}".format(i, len(df), folder, uuid), end="")

        file = open(os.path.join("urlscan", folder, uuid, "dom_page.html"))
        outer = BeautifulSoup(file.read(), "html.parser")
        file.close()

        html = outer.pre.text
        html = html.replace(" ", "")    # delete space
        html = html.replace("\n", "")    # delete end line
        html = html.replace("\t", "")    # delete tab

        hash_value = sha1_hash(html)
        df.loc[i, "hash_value"] = hash_value

    df.to_csv("url_unique.csv", index=False)
    print("\nEnd hash")

if __name__ == "__main__":
    main()