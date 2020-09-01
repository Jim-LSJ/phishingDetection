import pandas as pd
import os, sys
df = pd.read_csv(os.path.join(sys.argv[1], "verified_online.csv"))   # URL/20200826/PhishTank

date = sys.argv[1][4:8] + "-" + sys.argv[1][8:10] + "-" + sys.argv[1][10:12]
urls = []
for i in range(len(df)):
    if df.loc[i, "submission_time"][0:10] == date:
        urls.append(df.loc[i, "url"])

f = open(os.path.join(sys.argv[1], "new_url.txt"), "w")

for url in urls:
    f.write(url + "\n")

f.close()