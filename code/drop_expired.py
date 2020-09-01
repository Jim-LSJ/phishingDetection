import pandas as pd
import os, sys

df = pd.read_csv(sys.argv[1])
d = pd.DataFrame()
for i in range(len(df)):
    if df.loc[i, "UUID"] + ".png" in os.listdir("screenshot/" + sys.argv[1].split("/")[1]):
        d = d.append(df.loc[i])

d.to_csv(sys.argv[1], index=False)

## Usage: python3 code/drop_expired.py URL/20200829/feature.csv