import os, sys
import pandas as pd

df = pd.read_csv(os.path.join("URL", "feature.csv"))

f = open(os.path.join(sys.argv[1], "OpenPhish", "feed.txt"))
urls = f.read().split('\n')[:-1]
f.close()

urls_data = df["URL"].tolist()
f_out = open(os.path.join(sys.argv[1], "OpenPhish", "new_feed.txt"), "w")
for url in urls:
    if url in urls_data:
        continue
    f_out.write(url + "\n")

f_out.close()

PT = pd.read_csv(os.path.join(sys.argv[1], "PhishTank", "verified_online.csv"))
f_out = open(os.path.join(sys.argv[1], "PhishTank", "new_url.txt"), "w")
for url in PT["url"]:
    if url in urls_data:
        continue
    f_out.write(url + "\n")

f.close()

print("Finish Check!")
## Usage python3 code/check_url.py <URL/20200710>